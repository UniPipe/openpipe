"""
Produce the item supplied as parameter
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    item # The item to be inserted, default is the input item
    """

    # Output the configuration item
    def on_input(self, item):
        if isinstance(self.config, list):
            for list_item in self.config:
                self.put(list_item)
        else:
            self.put(self.config)
