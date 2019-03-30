"""
Build a dictionary from a key/map regex group expression
"""
from openpipe.pipeline.engine import ActionRuntime
from re import compile, MULTILINE


class Action(ActionRuntime):

    category = "Data Transformation"

    required_config = """
    regex:      # A regex expression that must match two groups:
                # (group1) (group2)
    """

    def on_start(self, config):
        # Compile regex to improve efficiency
        self.regex = compile(config["regex"], MULTILINE)

    def on_input(self, item):
        new_item = {}
        for key, value in self.regex.findall(item):
            new_item[key] = value
        self.put(new_item)
