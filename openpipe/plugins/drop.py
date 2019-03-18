"""
Produce the input item after removing some fields
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_params = """
    []  # List of keys for the fields to be removed
    """

    # Output the parameters item
    def on_input(self, item):
        new_item = {}
        for key, value in item.items():
            if key not in self.params:
                new_item[key] = value
        self.put(new_item)
