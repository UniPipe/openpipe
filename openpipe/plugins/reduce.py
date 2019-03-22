"""
Produce single units resulted from reducing an item
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The target reduction format
    """

    def on_input(self, item):
        if isinstance(item, dict):
            new_item_key = self.config[0]
            new_item_value = self.config[1]
            for key, value in item.items():
                new_item = {new_item_key: key, new_item_value: value}
                self.put(new_item)
