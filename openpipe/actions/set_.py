"""
Set value(s) for key(s)
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Transformation"

    required_some_config = """
    # The action configuration must be a transformation dictionary in the format:
    #   key_name1: value1
    #       ...
    #   key_name2: value2
    #
    """

    def on_input(self, item):
        new_item = item
        for key_name, value in self.config.items():
            new_item[key_name] = value
        self.put(new_item)
