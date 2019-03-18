"""
_Abort execution when input does not match expected values
"""

from sys import stderr
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_params = """
    """

    def on_start(self, params):
        self.start_params = params  # Typically on_finish does not use params
        self.never_called = True
        self.check_index = 0

    def on_input(self, item):
        if isinstance(self.params, list):
            expected_count = len(self.params)
            if self.check_index >= expected_count:
                raise AssertionError("Test expected %d items, got %d" % (expected_count, self.check_index+1))
            self.value_assert(item, self.params[self.check_index])
            self.check_index += 1
        else:
            self.value_assert(item, self.params)
        self.never_called = False

    def on_finish(self, reason):
        if self.never_called:
            print("Failed on_finish", self.plugin_label, file=stderr)
            raise Exception("Did not receive any item, expected:\n" + str(self.start_params))
        if isinstance(self.params, list) and self.check_index < len(self.start_params):
            print("Failed on_finish", self.plugin_label, file=stderr)
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
                            (str(value), str(key), str(item_value)), file=stderr
                        )
                    raise
        else:
            try:
                assert(item == assert_data)
            except AssertionError:
                print("AssertionError: Expected %s, got %s" % (str(assert_data), str(item)), file=stderr)
                raise
        self.put(item)
