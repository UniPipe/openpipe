"""
Iterate the configuration item producing each element
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The item to be iterated over
    """

    def on_input(self, item):
        if isinstance(self.config, list):
            for item in self.config:
                self.put(item)
        else:
            for key, value in self.config.items():
                new_item = {"key": key, "value": value}
                self.put(new_item)
