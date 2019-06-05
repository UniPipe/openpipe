"""
Remove a file
"""
from openpipe.pipeline.engine import ActionRuntime
from os import unlink


class Action(ActionRuntime):

    category = "Data Control"

    required_config = """
    path:     # Full path of the file to be removed
    """

    def on_input(self, item):
        unlink(self.config["path"])
        self.put(item)
