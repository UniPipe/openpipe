"""
Produce selected input items based on in/out conditions
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
        in: True        # Expression to select items
        out: False      # Expression to exclude items
    """

    def on_input(self, item):
        if self.config['in'] and not self.config['out']:
            self.put(item)
