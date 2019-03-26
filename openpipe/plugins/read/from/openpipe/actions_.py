"""
Produce the list of available action plugins
"""
from openpipe.pipeline.engine import PluginRuntime
from openpipe.utils import get_actions


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The item to be printed, the default is the input item
    """

    def on_input(self, item):
        for action in get_actions():
            self.put(action)