"""
Produce the merge between the input item and config item
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    item # The item to be inserted, default is the input item
    """

    def on_input(self, item):
        first_item = item
        second_item = self.config
        # If first item is a list, we need to merge against each list item
        if isinstance(first_item, list):
            for first_item in first_item:
                # Second item may also be a list, produce the result
                if isinstance(second_item, list):
                    for second_item in second_item:
                        self.put({**first_item, **second_item})
                else:
                    self.put({**first_item, **second_item})
        # If second item is a list, we need to merge against each list item
        elif isinstance(second_item, list):
            for second_item in second_item:
                # First item may also be a list, produce the result
                if isinstance(first_item, list):
                    for first_item in second_item:
                        self.put(**first_item, **second_item)
                else:
                    self.put({**first_item, **second_item})

        else:
            # Simpler case is a dict merge with dict
            self.put({**first_item, **second_item})
