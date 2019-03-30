"""
Produce the list of files matching a pattern
"""
from openpipe.pipeline.engine import ActionRuntime
from glob import glob
from os.path import normpath


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The pattern to be used for matching
    """

    def on_input(self, item):
        glob_pattern = normpath(self.config)
        file_list = sorted(glob(glob_pattern))
        self.put(file_list)
