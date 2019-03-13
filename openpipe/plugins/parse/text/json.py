"""
Produce dictionary items from JSON input items
"""
from json import loads
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    content:        # Content to be parsed to json
    """

    def on_input(self, item):
        json_content = loads(self.config['content'])
        self.put(json_content)
