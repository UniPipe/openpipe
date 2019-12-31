"""
Produce "True" when the input is empty
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    def on_input(self, item):
        pass

    def on_finish(self, item):
        self.put(True)
