"""
Produce the configuration item
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    $_$     # The item to be inserted
    """

    # Output the config item
    def on_input(self, item):
        self.put(self.config)
