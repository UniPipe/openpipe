"""
Produce dictionary with input joined to params
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_params = """ YES
    """

    # Output the parameters item
    def on_input(self, item):
        for extend_item in self.params:
            new_item = {**item, **extend_item}
            self.put(new_item)
