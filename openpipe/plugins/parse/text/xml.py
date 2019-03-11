"""
Produce ordered dictionary items from XML input items
"""
import xmltodict
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):
    default_config = """
    $_$     # The content to be parsed
    """

    def on_input(self, item):
        self.put(xmltodict.parse(self.config))
