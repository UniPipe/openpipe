"""
Remove some keys from the tag item
"""

from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = (
        "# name or list of names of the keys to be remove from the tag dict"
    )

    # Output the config item
    def on_input(self, item):
        current_tag = self._tag

        new_item = {}
        drop_list = self.config
        if not isinstance(drop_list, list):
            drop_list = [drop_list]
        for key in drop_list:
            del current_tag[key]
            self.set_tag(current_tag)
        self.put(new_item)
