"""
Insert item in the pipeline
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The item to be inserted, default is the input item
    """

    # Output the configuration item
    def on_input(self, item):
        if isinstance(self.config, list):
            for list_item in self.config:
                self.put(list_item)
        else:
            self.put(self.config)
