"""
Join items from an input list item
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The string to be used for joining elements
    """

    def on_input(self, item):
        new_item = item
        # If input elements are not strings, convert them
        if not isinstance(item[0], str):
            new_item = [str(x) for x in item]
        self.put(self.config.join(new_item))
