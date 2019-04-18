import threading
from os import environ
from queue import Queue
from openpipe.utils import create_action_instance

DEBUG = environ.get("DEBUG")


class SegmentRunner(threading.Thread):
    def __init__(self, segment_name, thread_number, input_queue):
        threading.Thread.__init__(self)
        self.name = segment_name
        self.input_queue = input_queue
        self.control_in = Queue()
        self.control_out = Queue()
        self.action_list = []

    def get(self):
        return self.control_out.get()

    def run(self):
        """ Run the on start method for all the actions in this segment """
        print("SEG RUNNER", self.action_list)
        for i, action in enumerate(self.action_list):
            action.action_label = "Thread-'" + self.name + "' :" + action.action_label
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    print("on_start %s " % action.action_label)
                try:
                    action.controller_queue = self.controller_queue
                    on_start_func(action.initial_config)
                    action._segment_linker = None
                except:  # NOQA: E722
                    self.control_out.put(("failed", action.action_label))
                    return
        self.control_out.put(None)

    def add_action(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label
        )
        self.action_list.append(action_instance)
