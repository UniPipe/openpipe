"""
Replace some phrase with other phrase
"""
from openpipe.pipeline.engine import PluginRuntime
from openpipe.utils import is_nested_dict


class Plugin(PluginRuntime):

    required_some_config = """
    # The replacement rules dictionary
    """

    def on_start(self, config):
        if is_nested_dict(config):
            self.on_input = self.on_input_dict

    def on_input(self, item):
        for key, value in self.config.items():
            item = item.replace(key, value)
        self.put(item)

    def on_input_dict(self, item):
        for item_key, replace_dict in self.config.items():
            for key, value in replace_dict.items():
                item[item_key] = item[item_key].replace(key, value)
        self.put(item)
