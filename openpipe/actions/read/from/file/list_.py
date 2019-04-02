"""
Produce the list of files matching a pattern
"""
from openpipe.pipeline.engine import ActionRuntime
from pathlib import Path


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The pattern to be used for matching
    """

    def on_input(self, item):
        file_list = sorted(Path(".").glob(self.config))
        file_list = [filename.as_posix() for filename in file_list]
        self.put(file_list)
