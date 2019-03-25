"""
Replaces some phrase with other phrase
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    # Replacement rules ditcionary
    """

    def on_input(self, item):
        print(self.config)
        self.put(item)
