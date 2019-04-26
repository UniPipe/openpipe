import threading
from traceback import format_exc
from os import environ
from queue import Queue
from openpipe.utils import create_action_instance

DEBUG = environ.get("DEBUG")


class SegmentRunner(threading.Thread):
    def __init__(self, segment_name, thread_number, input_queue_list):
        threading.Thread.__init__(self)
        self.name = segment_name
        self.input_queue_list = input_queue_list.copy()
        self.input_iter = iter(self.input_queue_list)
        self.control_in = Queue()
        self.control_out = Queue()
        self.action_list = []

    def get(self):
        return self.control_out.get()

    def run(self):
        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            action.action_label = "Thread-'" + self.name + "' :" + action.action_label
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    print("on_start %s " % action.action_label)
                try:
                    on_start_func(action.initial_config)
                except:  # NOQA: E722
                    detail = format_exc()
                    failed_reply = ("failed", action.action_label, detail)
                    self.control_out.put(failed_reply)
                    return
        start_reply = ("started", i, None)
        self.control_out.put(start_reply)
        while True:
            # Wait for some input element before getting into "running"
            request = self.control_in.get()
            raise NotImplementedError(request)
        self.loop_on_input_data()

    def loop_on_input_data(self):
        while True:
            item = self.get_next_input.get()
            if item is None:
                break

    def get_next_input(self):
        """ Retrieve the next available input item """
        if self.current_queue is None:
            current_iter = self.input_iter = iter(self.input_queue_list)
            current_queue = self.current_queue = next(current_iter)
        else:
            current_queue = self.current_queue
        while True:
            # Wait 0.5s before going for next queue check
            current_queue.get(timeout=0.5)

    def add_action(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label, self.get_resource
        )
        self.action_list.append(action_instance)

    def get_resource(self, request):
        self.control_out.put(request)
