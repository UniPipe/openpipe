"""
Merge input and configuration items
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_tag$ # The item to merge with
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
