"""
Produce input item after removing some fields
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    default_config = """
    []  # List of keys for the fields to be removed
    """

    # Output the configuration item
    def on_input(self, item):
        new_item = {}
        for key, value in item.items():
            if key not in self.config:
                new_item[key] = value
        self.put(new_item)
