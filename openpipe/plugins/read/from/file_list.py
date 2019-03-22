"""
Produce the list of files matching a pattern
"""
from openpipe.pipeline.engine import PluginRuntime
from glob import glob


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The pattern to be used for matching
    """

    def on_input(self, item):
        for filename in glob(self.config):
            self.put(filename)
