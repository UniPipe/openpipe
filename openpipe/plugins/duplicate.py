"""
Duplicate the input items into one or more segments
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_start(self, config, segment_resolver):
        self.target_segment = segment_resolver(config)

    def on_input(self, item):
        self.put(item)
        self.put_target(item, self.target_segment)

    def on_complete(self):
        self.put_target(None, self.target_segment)
