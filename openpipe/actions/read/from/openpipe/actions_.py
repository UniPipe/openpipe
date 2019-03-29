"""
Produce the list of available action actions
"""
from openpipe.pipeline.engine import ActionRuntime
from openpipe.utils import get_actions_metadata


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The item to be printed, the default is the input item
    """

    def on_input(self, item):
        for action in get_actions_metadata():
            self.put(action)
