"""
If input item is not a list, convert it into a single item list
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):
    required_config = """
    key:     # Key of the field that must be a list
    """

    def on_input(self, item):
        key_name = self.config['key']
        key_item = item[key_name]
        if not isinstance(key_item, list):
            item[key_name] = [key_item]
        self.put(item)
