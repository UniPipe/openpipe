"""
If an input field is not a list, transform it into a single item list
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        key_name = self.config
        key_item = item[key_name]
        if not isinstance(key_item, list):
            item[key_name] = [key_item]
        self.put(item)
