from openpipe.core import PluginRuntimeCore
"""
This file provides the core class for a plugin instance
"""


class PluginRuntime(PluginRuntimeCore):

    def init(self):
        self.next_step = None

    def put(self, item):

        # Put on next
        if self.next_step:
            self.next_step._on_input(item)

    def put_target(self, item, target):
        target._on_input(item)
