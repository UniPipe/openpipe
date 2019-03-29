"""
Produce the list of files matching a pattern
"""
from openpipe.pipeline.engine import ActionRuntime
from glob import glob


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The pattern to be used for matching
    """

    def on_input(self, item):
        file_list = sorted(glob(self.config))
        self.put(file_list)
