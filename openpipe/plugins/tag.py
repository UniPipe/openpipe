"""
Tag input item with the provided configuration tag item
"""

from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     #  Default is to tag the entire input item
    """

    def on_input(self, item):
        self.set_tag(self.config)
        self.put(item)
