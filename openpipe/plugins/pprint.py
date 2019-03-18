"""
Pretty print an item
"""

from openpipe.engine import PluginRuntime
from pprint import pprint


class Plugin(PluginRuntime):

    # The default behavior is to print the input item
    optional_params = """
    $_$     # The content to be pretty printed
    """

    def on_input(self, item):
        pprint(self.params)
        self.put(item)
