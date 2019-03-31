"""
Select input items based on a conditional expression
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Selection"

    required_some_config = """ # Boolean Expression
    # Items are only copied to next action only when the expression evaluates
    # to True
    """

    def on_input(self, item):
        if self.config:
            self.put(item)
