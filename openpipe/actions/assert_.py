"""
Asserts that input matches the config provided item
"""

from sys import stderr
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Validation"

    required_some_config = """
    # The item with the expected value(s)
    """

    def on_start(self, config):
        if isinstance(config, list):
            self.expected_count = len(config)
        else:
            self.expected_count = 1
        # For asserts on list of items, we need to keep the current index
        # on a per tag basis
        self.tag_assert_idx = {}  # We keep the index
        self.is_bool = False

    def on_input(self, item):
        config = self.config
        if isinstance(config, bool):
            self.value_assert(item, config)
            return

        # Treat single items as lists of one item
        if not isinstance(config, list):
            config = [config]

        # We can't assert on dict based tags
        if isinstance(self._tag, dict):
            tag_index = None
        else:
            tag_index = self._tag
        current_index = self.tag_assert_idx.get(tag_index, 0)
        if current_index >= self.expected_count:
            raise AssertionError(
                "Test expected %d items, got %d"
                % (self.expected_count, current_index + 1)
            )
        self.value_assert(item, config[current_index])
        self.tag_assert_idx[tag_index] = current_index + 1

    def on_finish(self, reason):
        if self.is_bool:
            return

        for context_value, context_index in self.tag_assert_idx.items():
            if context_index < self.expected_count:
                raise AssertionError(
                    "Test [%s] expected %d items, got %d"
                    % (context_value, self.expected_count, context_index + 1)
                )

    def value_assert(self, item, assert_data):
        assert assert_data is not None
        if isinstance(assert_data, bool):
            assert assert_data
            self.put(item)
            return
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
