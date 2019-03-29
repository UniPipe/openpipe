"""
Sort items by keys
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_config = """
    key:                    # Name or list of names to use a group key
    """

    optional_config = """
    descendent: False       # Use descendent order ?

    # It is possible to identify groups of repeated keys by setting
    # key_on_first. When it's set, the key will only be present on the
    # first item of a group items with the repeated key
    key_on_first: False
    """

    def on_start(self, config):
        self.data = []
        self.descendent = config["descendent"]

    def on_input(self, item):
        # we must copy because the item may be changed in the thread
        key_value = item[self.config["key"]]
        self.data.append((key_value, item.copy()))

    def on_finish(self, reason):
        self.data.sort(key=lambda x: x[0], reverse=self.descendent)
        last_key_value = None
        for key, item in self.data:
            key_value = item[self.config["key"]]
            if self.config["key_on_first"]:
                if key_value == last_key_value:
                    del item[self.config["key"]]
                last_key_value = key_value
            self.put(item)
