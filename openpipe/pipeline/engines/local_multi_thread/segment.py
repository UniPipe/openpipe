""" This module provides the segment management classes """

from os import environ
from queue import Queue
from threading import Thread
from pprint import pprint
from .runner import SegmentRunner


DEBUG = environ.get("DEBUG")

MAX_THREADS_PER_SEGMENT = int(environ.get("MAX_THREADS_PER_SEGMENT", "10"))
QSIZE_CHECK_INTERVAL = 1  # Interval between qsize checks
QSIZE_THREAD_TRIGGER = 2  # Qsize to trigger that should trigger a new thread


class SegmentController(Thread):
    """
    The segment controller runs on it's own thread, it loops waiting for messages
    on its input bus. To ensure thread safety, once started, all interactions with the
    bus must be performed through the submit_message() method.
    """

    class SegmentInfo:
        """ Placeholder for a segment control information """

        def __init__(self):
            self.input_queue = Queue()  # The queue used to deliver input items
            self.input_link_count = 0  # Number of received links requests
            self.thread_list = []  # List of segment runner threads
            self.action_list = []  # List of the segment actions config

        def add_action(self, action_name, action_config, action_label):
            self.action_list.append((action_name, action_config, action_label))

    def __init__(self, output_queue: Queue):
        Thread.__init__(self)
        self.segment_info = {}  # Dictionary with segment info objects
        self._input_queue = Queue()
        self.output_queue = output_queue

    def submit_message(self, **kwargs):
        self._input_queue.put(kwargs)

    def create_segment(self, segment_name):
        self.segment_info[segment_name] = control = self.SegmentInfo()
        return control

    def run(self):
        while True:
            message = self._input_queue.get()
            try:
                cmd = message["cmd"]
                handle_func_name = "_handle_" + (cmd.replace(" ", "_"))
            except TypeError:
                print("Got invalid message:", message)
                raise
            if cmd == "terminate":
                return
            # The following commands are directly delivered tro the client
            if cmd in ["error", "log", "started", "debug", "finished"]:
                self.output_queue.put(message)
            else:
                del message["cmd"]
                try:
                    getattr(self, handle_func_name)(**message)
                except:  # NOQA: E722
                    print("CMD", cmd)
                    print("Error processing message:")
                    pprint(message)
                    raise

    def _handle_end_of_link(self, segment, reply_queue):
        segment_info = self.segment_info[segment]
        segment_info.input_link_count -= 1

        if segment_info.input_link_count > 0:
            reply = True
        else:
            reply = False
            self.output_queue.put({"cmd": "completed", "segment_name": segment})
        reply_queue.put(reply)

    def _handle_request_input_link(self, target_segment, reply_queue):
        segment_info = self.segment_info.get(target_segment, None)
        if segment_info is None:
            reply = None
        else:
            reply = input_queue = segment_info.input_queue
            thread_list = segment_info.thread_list
            # If this is the first request, create the runner thread
            if len(thread_list) == 0:
                try:
                    runner_thread = SegmentRunner(
                        segment_name=target_segment,
                        action_list=segment_info.action_list,
                        thread_number=0,
                        input_queue=input_queue,
                        controller=self,
                    )
                except Exception:
                    reply = None
                else:
                    runner_thread.start()
        reply_queue.put(reply)
