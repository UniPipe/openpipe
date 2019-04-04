"""
Split a path to 'directory' and 'file' components
"""
from os.path import split
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    # The default behavior is to print the input item
    optional_config = """
    $_$     # The path to produce the director name from
    """

    def on_input(self, item):
        directory, file = split(self.config)
        new_item = {"directory": directory, "file": file}
        self.put(new_item)
