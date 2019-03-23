"""
Abort execution when input does not match the expected value
"""

from sys import stderr
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    """

    def on_start(self, config):
        self.expected_count = len(config) if isinstance(config, list) else 1
        self.context_assert_index = {}

    def on_input(self, item):
        config = self.config

        # Treat single items as lists of one item
        if not isinstance(config, list):
            config = [config]

        current_index = self.context_assert_index.get(self.context_item, 0)
        if current_index >= self.expected_count:
            raise AssertionError(
                "Test expected %d items, got %d"
                % (self.expected_count, current_index + 1)
            )
        self.value_assert(item, config[current_index])
        self.context_assert_index[self.context_item] = current_index + 1

    def on_finish(self, reason):
        for context_value, context_index in self.context_assert_index.items():
            if context_index < self.expected_count:
                raise AssertionError(
                    "Test [%s] expected %d items, got %d"
                    % (context_value, self.expected_count, context_index + 1)
                )

    def value_assert(self, item, assert_data):
        assert assert_data is not None
        if isinstance(assert_data, dict):
            for key, value in assert_data.items():
                item_value = item.get(key)
                try:
                    assert item_value == value
                except AssertionError:
                    try:
                        value_len = len(value)
                    except TypeError:
                        value_len = 0
                    try:
                        item_value_len = len(item_value)
                    except TypeError:
                        item_value_len = 0
                    print(
                        "AssertionError: On field '%s' expected %s[%s] %s , got %s[%s] %s"
                        % (
                            str(key),
                            type(value),
                            value_len,
                            str(value),
                            type(item_value),
                            item_value_len,
                            str(item_value),
                        ),
                        file=stderr,
                    )
                    raise
        else:
            try:
                assert item == assert_data
            except AssertionError:
                print(
                    "AssertionError: Expected %s, got %s"
                    % (str(assert_data), str(item)),
                    file=stderr,
                )
                raise
        self.put(item)
