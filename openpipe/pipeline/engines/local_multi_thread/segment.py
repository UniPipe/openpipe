""" This module provides the segment management classes """

import threading
from os import environ
from openpipe.utils import create_action_instance
from time import time
from queue import Queue
from .runner import SegmentRunner


DEBUG = environ.get("DEBUG")

MAX_THREADS_PER_SEGMENT = int(environ.get("MAX_THREADS_PER_SEGMENT", "10"))
QSIZE_CHECK_INTERVAL = 1  # Interval between qsize checks
QSIZE_THREAD_TRIGGER = 2  # Qsize to trigger that should trigger a new thread


class PipelineSegmentRun(threading.Thread):
    def __init__(self, segment_name, controller_queue):
        threading.Thread.__init__(self, segment_name)
        self.action_list = []
        self.control_queue = Queue()
        self.controller_queue = controller_queue

    def add(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label
        )
        self.action_list.append(action_instance)

    def run(self):
        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            action.action_label = (
                "Thread-'" + self.segment_name + "' :" + action.action_label
            )
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    print("on_start %s " % action.action_label)
                try:
                    action.controller_queue = self.controller_queue
                    on_start_func(action.initial_config)
                    action._segment_linker = None
                except:  # NOQA: E722
                    self.control_queue.put(("failed", action.action_label))
                    return
        self.control_queue.put(("started", i))


class SegmentController(threading.Thread):

    def __init__(self, segment_name):
        threading.Thread.__init__(self)
        self.segment_name = segment_name
        self.control_queue = Queue()
        self.thread_list = []
        self.action_config_list = []
        self.input_queue_list = []
        self.action_list = []

    def input_request(request):
        pass

    def run(self):
        # First we send all the ones we need
        # Then we wait for link requests

        while True:
            requester = self.control_in.get()
            if requester is None:
                break
            input_queue = Queue()
            self.input_queue_list.append(input_queue)
            self.control_out.send("INACTIVE")

        # Got no input requests
        if len(self.input_queue_list) > 0:
            self.control_out.send("INACTIVE")
            return

        # Now let's run the start code, which may send input requests
        run_thread = SegmentRunner(self.segment_name, self, self.input_queue_list)
        for action_item in self.action_list:
            run_thread.add(action_item)

        # Signal that our start was completed
        #  request = self.control_out.send("STARTED")

        while True:
            run_thread.input_queue.get()

    def add(self, action_name, action_config, action_label):
        self.action_config_list.append((action_name, action_config, action_label))


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

        self._segment_linker = self._segment_linker

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
