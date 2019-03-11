"""
Remove some part from the input item
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    # Output the configuration item
    def on_input(self, item):
        new_item = {}
        for key, value in item.items():
            if key not in self.config:
                new_item[key] = value
        self.put(new_item)
