"""
Remove some keys from the input item
"""

from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    []  # List of keys for the fields to be removed
    """

    # Output the config item
    def on_input(self, item):
        new_item = {}
        for key, value in item.items():
            if key not in self.config:
                new_item[key] = value
        self.put(new_item)
