"""
Produce list by splitting an input string
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Transformation"

    optional_config = """
        separator: " "          # String used to separate fields
        max_split: -1           # Maximum number of split operations
        field_list: []          # List of keys to to be used for each value
    """

    def on_start(self, config):
        self.separator = config["separator"]
        self.max_splits = config["max_split"]
        self.field_list = config["field_list"]

    def on_input(self, item):
        new_item = item.split(self.separator, self.max_splits)
        if self.field_list:
            new_dict_item = {}
            for i, key in enumerate(self.field_list):
                new_dict_item[key] = new_item[i]
        else:
            self.put(new_item)
