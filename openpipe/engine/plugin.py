from openpipe.core import PluginRuntimeCore
"""
This file provides the core class for a plugin instance
"""


class PluginRuntime(PluginRuntimeCore):

    def init(self):
        self.next_step = None
        self.extra_steps = []
        self.conditional_steps = []

    def put(self, item):

        # Put on next
        if self.next_step:
            self.next_step._on_input(item)

        # Put on other other references
        for next_step in self.extra_steps:
            next_step._on_input(item)
