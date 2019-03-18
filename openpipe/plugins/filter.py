"""
Filter in/out items using expressions
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
        in: True        # Expression to select items to be delivered to the next step
        out: False      # Expression to exclude items to be delivered to the next step
    """

    def on_input(self, item):
        if self.config['in'] and not self.config['out']:
            self.put(item)
