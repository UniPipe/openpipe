"""
Produce a list by queuing items
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The count of items to be queued before producing a list
    """

    def on_start(self, config):
        self.queue = []

    def on_input(self, item):
        self.queue.append(item)
        if len(self.queue) == self.config:
            self.put(self.queue)
            self.queue = []
