"""
Print content
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The content to be printed, default is the input item
    """

    def on_input(self, item):
        print(self.config)
        self.put(item)
