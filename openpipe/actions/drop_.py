"""
Remove some keys from the input item
"""

from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = "# name or list of names of the keys to be removed"

    # Output the config item
    def on_input(self, item):
        new_item = {}
        drop_list = self.config
        if not isinstance(drop_list, list):
            drop_list = [drop_list]
        for key, value in item.items():
            if key not in self.config:
                new_item[key] = value
        self.put(new_item)
