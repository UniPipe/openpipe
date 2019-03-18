"""
Produce the action's parameter item
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_params = """
    item # The item to be inserted, default is the input item
    """

    # Output the parameters item
    def on_input(self, item):
        if isinstance(self.params, list):
            for list_item in self.params:
                self.put(list_item)
        else:
            self.put(self.params)
