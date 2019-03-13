"""
Produce the count of input elements
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    ""   # The field name to store the count value
    """

    def on_start(self, config):
        self.count = 0

    def on_input(self, item):
        self.count += 1
        if self.config:
            new_item = item.copy()
            new_item[self.config] = self.count
            self.put(new_item)
        else:
            self.put(self.count)
