"""
Produce dictionary items from JSON input items
"""
from json import loads
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The content to be parsed
    """

    def on_input(self, item):
        new_item = loads(item)
        self.put(new_item)
