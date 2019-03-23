"""
Iterate the configuration item producing each element
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The item to be iterated over
    """

    def on_input(self, item):
        for item in self.config:
            self.put(item)
