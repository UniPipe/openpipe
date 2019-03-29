"""
Limit the max number of items sent to the next action
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Control"

    required_config = """
    max:    # The max number of items sent to next action
    """

    def on_start(self, config):
        self.count = 0

    def on_input(self, item):
        self.max = self.config["max"]
        if self.count == self.max:
            return
        self.count += 1
        self.put(item)
