"""
Produce items by iterating over an input key
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    requiredl_params = """
    key:    # A key name from the input item to be iterated
            # The output will be produced for each iteration item
    """

    def on_input(self, item):
        key = self.params['key']
        original_iterator = item[key]
        for iter_item in original_iterator:
            item[key] = iter_item
            self.put(item)
