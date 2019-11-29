"""
Update field values using case match
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = """ # Dictionary with the updates rules:
    #
    #   target_key_name:
    #       target_key_value: expression
    #
    #  Set target_key_name to target_key_value when expression evaluates
    #  to True
    """

    def on_input(self, item):
        new_item = item
        for target_key_name, target_key_values in self.config.items():
            for target_key_value, value in target_key_values.items():
                if value:
                    new_item[target_key_name] = target_key_value
                    break
        self.put(new_item)
