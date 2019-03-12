"""
Produce items by iterating over the content of a field
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # Item to be iterated
    """

    def on_input(self, item):
        original_iterator = self.config
        for iter_item in original_iterator:
            item[self.config] = iter_item
            self.put(item)
