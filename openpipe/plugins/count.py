"""
Produce the count of input elements received since start
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_params = """
    ""      # The default action is to output the current count value
            # If a key name is provided, the input item will be the output
            # With item[key] set to the count .
    """

    def on_start(self, params):
        self.count = 0

    def on_input(self, item):
        self.count += 1
        if self.params:
            new_item = item.copy()
            new_item[self.params] = self.count
            self.put(new_item)
        else:
            self.put(self.count)
