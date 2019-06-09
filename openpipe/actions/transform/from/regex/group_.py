"""
Build a dictionary from a key/map using regex groups
"""
from openpipe.pipeline.engine import ActionRuntime
from re import compile, MULTILINE


class Action(ActionRuntime):

    category = "Data Transformation"

    required_some_config = """
    dictionary: # A dictionary in the format:
                #   key_name: regex_with_group_matchin_value
    """

    def on_start(self, config):
        # Compile regex to improve efficiency
        self.regex_dict = {}
        for key, value in config:
            self.regex_dict[key] = compile(config["value"], MULTILINE)

    def on_input(self, item):
        new_item = {}
        for key, value in self.regex_dict:
            new_item[key] = self.regex_dict[key].findall(item)[0]
