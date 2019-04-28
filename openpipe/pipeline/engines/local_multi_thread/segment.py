""" This module provides the segment management classes """

import threading
from os import environ
from time import time
from queue import Queue
from threading import Thread
from .runner import SegmentRunner


DEBUG = environ.get("DEBUG")

MAX_THREADS_PER_SEGMENT = int(environ.get("MAX_THREADS_PER_SEGMENT", "10"))
QSIZE_CHECK_INTERVAL = 1  # Interval between qsize checks
QSIZE_THREAD_TRIGGER = 2  # Qsize to trigger that should trigger a new thread


class SegmentManager(Thread):
    """
    The segment manager runs on it's own thread, it loops waiting for message
    from it's input bus. To ensure thread safety, all interactions with the
    segment manager are performed through submit_message()

    The following messages are supported:

    The following message will be sent to the tartet segment controller input queue

        A segment controller/pipeline client requests an input link to a segment:
            submit_message(type="request input link", segment="name", reply_link=reply_queue)

    The following messages will be sent to the "output" queue.
        A segment controller requests the action list for a segment:
            submit_message(type="get action list", segment="name", reply_link=reply_queue)
        A segment controller reports that an action segment was started with success:
            submit_message(type="started", segment="start", start_time=120s)
        A segment controller reports that an action segment received end of input:
            submit_message(type="finished", segment="start", reply_link=input_queue)
        A segment controller reports that an error happened:
            submit_message(type="error", where="on_start", message=120s)
    """

    def __init__(self):
        self.controllers = []
        self._input_queue = Queue()

    def submit_message(self, **kwargs):
        self._input_bus.put(kwargs)

    def run(self, output_queue):
        message = self._input_bus.get()
        print(message)


class SegmentController(threading.Thread):
    def __init__(self, segment_name):
        threading.Thread.__init__(self)
        self.name = "Controller_" + segment_name
        self.control_in = Queue()
        self.control_out = Queue()
        self.segment_name = segment_name
        self.control_queue = Queue()
        self.thread_list = []
        self.action_config_list = []
        self.input_queue_list = []

    def get(self):
        return self.control_out.get()

    def put(self, *args, **kwargs):
        return self.control_in.put(*args, **kwargs)

    def provide_input_to(self, reply_queue):
        input_queue = Queue()
        self.input_queue_list.append(input_queue)
        reply_queue.put(input_queue)

    def run(self):
        # Create a runner thread
        runner_thread = SegmentRunner(self.segment_name, 0, self.input_queue_list)

        # Add all actions to the runner thread
        for action_name, action_config, action_label in self.action_config_list:
            runner_thread.add_action(action_name, action_config, action_label)
        runner_thread.start()

        # Wait for link requests from the runner thread
        while True:
            start_reply = runner_thread.get()
            status, title, detail = start_reply
            # Send link requests to the pipeline manager
            self.control_out.put(start_reply)
            if status == "started":
                break

        # Waiting for all dependent segments to be started
        start_reply = self.control_in.get()
        assert start_reply == "running"
        self.thread_list.append(runner_thread)

    def add_action(self, action_name, action_config, action_label):
        self.action_config_list.append((action_name, action_config, action_label))

    def activate(self, activation_arguments):
        """ Activate a segment by sending the activation item to the input """
        self.input_queue_list[0].put(activation_arguments)


class PipelineSegment(threading.Thread):
    def __init__(self, segment_name, thread_number):
        threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.input_queue_list = []
        self.control_queue = Queue()
        self.name = segment_name
        self.segment_name = segment_name
        self.action_list = []
        self.config_list = []
        self.input_sources = []
        self.lock_sources = threading.RLock()
        self.thread_count = 0
        self.lock_thread_count = thread_number
        self.base_segment_info = []

    def activate(self, activate_arguments):
        if activate_arguments is not None:
            self.add_source(self)
        new_item = self, activate_arguments, {}
        self.input_queue.put(new_item)

    def add_source(self, source):
        with self.lock_sources:
            self.input_sources.append(source)

    def run(self):

        self.loop_on_input_data()

    def loop_on_input_data(self):

        previous_time = time()

        # Loop waiting for input
        while True:
            item = self.input_queue.get()
            source, input_item, tag = item

            if input_item is None:

                # If we are not thread 0, we simply repeat the None and terminate
                # The repeated None will be used be consumed by the remaning
                # threads on the pool that need to die
                if self.thread_number != 0:
                    print("GOT NONE KILLING ME", self, self.thread_number)
                    self.input_queue.put(item)
                    self.control_queue.put((None, self))
                    return

                if source is not None:
                    with self.lock_sources:
                        self.input_sources.remove(source)
                self.action_list[0]._on_input(
                    source, None, tag
                )  # Send end-of-input «None» to trigger on_finish()
                with self.lock_sources:
                    if len(self.input_sources) == 0:
                        print("Killing me", self)
                        self.input_queue.task_done()
                        # Put None to kill any remaning threads in the pool
                        self.input_queue.put(item)
                        self.control_queue.put((None, self))
                        return
            else:
                current_time = time()
                elapsed_time = current_time - previous_time
                #  if self.thread_number == 0:
                #  input_qsize = self.input_queue.qsize()
                #  print("QSIZE", self, input_qsize, elapsed_time)
                #  If we are thread 0 and queue is increasing, report our size
                if (
                    self.thread_number == 0 and elapsed_time > QSIZE_CHECK_INTERVAL
                ):  # Only the first thread checks and reports status
                    input_qsize = self.input_queue.qsize()
                    control_qsize = self.control_queue.qsize()
                    # Don't send new qsize until a previous one was delivered
                    if control_qsize == 0 and input_qsize > QSIZE_THREAD_TRIGGER:
                        print("REPORTING needs queue", input_qsize)
                        self.control_queue.put((input_qsize, self))
                    previous_time = current_time

                self.action_list[0]._on_input(
                    source, input_item, tag
                )  # Send current time to the firs action to activate it
            self.input_queue.task_done()
