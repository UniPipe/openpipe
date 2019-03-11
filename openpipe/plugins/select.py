"""
Select input items matching a search condition
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        if isinstance(self.config, bool):
            if self.config is True:
                self.put(item)
        else:
            if self.config:
                self.put(self.config)
