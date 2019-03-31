"""
Insert an item
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    # Item to be produced as an output
    """

    # Output the config item
    def on_input(self, item):
        self.put(self.config)
