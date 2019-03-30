"""
Replace some phrase with other phrase
"""
from openpipe.pipeline.engine import ActionRuntime
from openpipe.utils import is_nested_dict


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = """ # Dictionary with the replacement rules:
    # Replacement rules for a single string input item:
    #
    #   { "search_string" : "replace_string", ... }
    #   Replaces all occurrences of search_string with replace_string
    #
    #   source_key_name:
    #       "search_string" : "replace_string"
    #
    #  In the 'source_key_name' value replaces all occurrences of
    # 'search_string' with 'replace_string' in the
    """

    def on_start(self, config):
        if is_nested_dict(config):
            self.on_input = self.on_input_dict

    def on_input(self, item):
        for key, value in self.config.items():
            item = item.replace(key, value)
        self.put(item)

    def on_input_dict(self, item):
        for item_key, replace_dict in self.config.items():
            for key, value in replace_dict.items():
                item[item_key] = item[item_key].replace(key, value)
        self.put(item)
