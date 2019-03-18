"""
Produce selected input items based on in/out conditions
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_params = """
        in: True        # Expression to select items
        out: False      # Expression to exclude items
    """

    def on_input(self, item):
        if self.params['in'] and not self.params['out']:
            self.put(item)
