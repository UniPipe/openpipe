import threading
from traceback import format_exc
from os import environ
from queue import Queue
from openpipe.utils import create_action_instance

DEBUG = environ.get("DEBUG")


class SegmentRunner(threading.Thread):
    def __init__(
        self, segment_name, action_list, thread_number, input_queue, controller
    ):
        threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.name = segment_name
        self.input_queue = input_queue
        self.controller = controller
        self.action_list = []
        self.linked_segments = []  # Segments for which a link was requested
        for action_name, action_config, action_label in action_list:
            self.add_action(action_name, action_config, action_label)

    def submit_message(self, **kwargs):
        self.controller.submit_message(**kwargs)

    def run(self):
        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            action.action_label = "Thread-'" + self.name + "' :" + action.action_label
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    self.submit_message(
                        cmd="debug", msg="on_start %s " % action.action_label
                    )
                try:
                    on_start_func(action.initial_config)
                except:  # NOQA: E722
                    detail = format_exc()
                    self.submit_message(cmd="error", where="on_start", msg=detail)
                    return
        self.submit_message(
            cmd="started", segment_name=self.name, thread_number=self.thread_number
        )
        self.loop_on_input_data()

    def loop_on_input_data(self):

        # Loop until no more input links are available
        first_action = self.action_list[0]
        input_links_available = True
        while input_links_available:
            item = self.input_queue.get()
            data_item, tag_item = item
            if data_item is None:
                reply_queue = Queue()
                self.controller.submit_message(
                    cmd="end_of_link", segment=self.name, reply_queue=reply_queue
                )
                input_links_available = reply_queue.get()
                if input_links_available:
                    continue
            first_action._on_input(data_item, tag_item)

        if self.thread_number == 0:
            # Send end_of_input to all requested links
            for queue in self.linked_segments:
                queue.put((None, None))

        self.controller.submit_message(cmd="finished", segment_name=self.name)

    def add_action(self, action_name, action_config, action_label):
        try:
            action_instance = create_action_instance(
                action_name, action_config, action_label, self
            )
        except Exception as ex:
            self.submit_message(cmd="error", where="module load", msg=str(ex))
            raise
            return
        action_instance.controller = self.controller
        if len(self.action_list) > 0:
            # Create the link from the previous actions
            self.action_list[-1].next_action = action_instance
        self.action_list.append(action_instance)

    def link_to(self, segment_name):
        reply_queue = Queue()
        self.controller.submit_message(
            cmd="request input link",
            target_segment=segment_name,
            reply_queue=reply_queue,
        )
        reply = reply_queue.get()
        self.linked_segments.append(reply)
        return reply
