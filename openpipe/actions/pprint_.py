"""
Pretty print an item
"""

from openpipe.pipeline.engine import ActionRuntime
from pprint import pprint


class Action(ActionRuntime):

    category = "Data Analysis"

    # The default behavior is to print the input item
    optional_config = """
    $_$     # The content to be pretty printed
    """

    def on_input(self, item):
        pprint(self.config)
        self.put(item)
