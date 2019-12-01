"""
Produce a list by queuing items
"""
from openpipe.pipeline.engine import ActionRuntime
from copy import copy

class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The count of items to be queued before producing a list.
    If set to 0 all items are queued until the input ends
    """

    def on_start(self, config):
        self.queue = []

    def on_input(self, item):
        new_item = copy(item)
        self.queue.append(new_item)
        if len(self.queue) == self.config:
            self.put(self.queue)
            self.queue = []

    def on_finish(self, item):
        if len(self.queue) > 0:
            self.put(self.queue)
