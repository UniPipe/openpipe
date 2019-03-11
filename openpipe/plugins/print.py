"""
Prints some content
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    default_config = """
    $_$     # The content to be printed
    """

    def on_input(self, item):
        print(self.config)
        self.put(item)
