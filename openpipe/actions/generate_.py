"""
Generate a range of numbers
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The count of numbers to be generated, starting from "0"
    """

    # Output the config item
    def on_input(self, item):
        for number in range(self.config):
            self.put(number)
