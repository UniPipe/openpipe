"""
Write item to context
"""

from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     #  Item to be stored as context, the default is the input item
    """

    def on_input(self, item):
        self.set_context(self.config)
        self.put(item)
