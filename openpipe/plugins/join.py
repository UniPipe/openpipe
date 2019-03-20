"""
Produce dictionary with input joined to config
"""

from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """ YES
    """

    # Output the parameters item
    def on_input(self, item):
        for extend_item in self.config:
            new_item = {**item, **extend_item}
            self.put(new_item)
