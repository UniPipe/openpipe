"""
Change item values when they match regular expressions
"""
from openpipe.pipeline.engine import ActionRuntime
import re


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_some_config = """ # Dictionary with the updates rules:
    #
    #   source_key_name:
    #       - 'regex_expression' : 'target_value'
    #
    #  When the 'source_key_name' value matches regex_expression
    #  replace it 'target_value'. Only the first match per key is applied.
    """

    def on_start(self, config):
        self.regex_dict = {}
        for source_key, regex_map_list in config.items():
            compiled_regex_map_list = self.regex_dict[source_key] = []
            for regex_dict in regex_map_list:
                regex, new_value = next(iter(regex_dict.items()))
                compiled_regex_map_list.append((re.compile(regex), new_value))

    def on_input(self, item):
        new_item = item
        for source_key, regex_map_list in self.regex_dict.items():
            source_value = item[source_key]
            for regex, new_value in regex_map_list:
                if regex.match(source_value):
                    new_item[source_key] = new_value
                    break
        self.put(new_item)
