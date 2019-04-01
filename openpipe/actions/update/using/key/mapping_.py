"""
Map values from source keys to values on target keys
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = """ # Dictionary with the key mapping :
    #
    #   target_key_name:
    #       source_key_name:
    #           old_value: new_value
    #
    #  The action will set the "target_key_name" to "new_value" when the value
    #  at source_key_name is equal to "old_value"
    """

    def on_input(self, item):
        for target_key_name, target_key_dict in self.config.items():
            for source_key_name, source_key_dict in target_key_dict.items():
                for old_value, new_value in source_key_dict.items():
                    if item[source_key_name] == old_value:
                        item[target_key_name] = new_value
        self.put(item)
