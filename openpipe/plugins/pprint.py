"""
Pretty print some content
"""

from openpipe.engine import PluginRuntime
from pprint import pprint


class Plugin(PluginRuntime):

    # The default behavior is to print the input item
    default_config = """
    $_$     # The content to be pretty printed
    """

    def on_input(self, item):
        pprint(self.config)
        self.put(item)
