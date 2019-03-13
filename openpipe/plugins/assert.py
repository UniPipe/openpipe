"""
Abort execution if input does not match expected values
"""

import sys
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    """

    def on_start(self, config, segment_resolver):
        self.start_config = config  # Typically on_complete does not use config
        self.never_called = True
        self.check_index = 0

    def on_input(self, item):
        if isinstance(self.config, list):
            expected_count = len(self.config)
            if self.check_index >= expected_count:
                raise AssertionError("Test expected %d items, got %d" % (expected_count, self.check_index+1))
            self.value_assert(item, self.config[self.check_index])
            self.check_index += 1
        else:
            self.value_assert(item, self.config)
        self.never_called = False

    def on_complete(self):
        if self.never_called:
            raise Exception("Did not receive any item, expected:\n" + str(self.start_config))
        if isinstance(self.config, list) and self.check_index < len(self.start_config):
            raise AssertionError("Test got less values than expected")

    def value_assert(self, item, assert_data):
        assert(assert_data is not None)
        if isinstance(assert_data, dict):
            for key, value in assert_data.items():
                item_value = item.get(key)
                try:
                    assert(item_value == value)
                except AssertionError:
                    print(
                            "AssertionError: Expected %s on field '%s', got %s" %
                            (str(value), str(key), str(item_value)), file=sys.stderr
                        )
                    raise
        else:
            try:
                assert(item == assert_data)
            except AssertionError:
                print("AssertionError: Expected %s, got %s" % (str(assert_data), str(item)), file=sys.stderr)
                raise
        self.put(item)
