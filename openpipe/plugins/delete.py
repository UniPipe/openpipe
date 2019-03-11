"""
Exclude input items from the input stream
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_start(self, config, segment_resolver):

        if isinstance(config, dict):
            self.on_input = self.on_input_dict

    def on_input(self, item):
        if self.config is False:
            self.put(item)

    def on_input_dict(self, item):
        self.where = self.config.get('where', None)

        # if matches the delete condition, do nothing
        if self.where is True:
            return

        self.put(item)
