"""
Produce list by splitting an input string
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Transformation"

    optional_config = """
        separator: " "          # String used to separate fields
        max_splits: -1          # Maximum number of split operations
    """

    def on_start(self, config):
        self.separator = config["separator"]
        self.max_splits = config["max_splits"]

    def on_input(self, item):
        new_item = item.split(self.separator, self.max_splits)
        self.put(new_item)
