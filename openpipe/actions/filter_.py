"""
Filter "what" depending on "in/out" conditions
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
        in: True    # Expression to include items
        out: False  # Expression to exclude items
        what: $_$   # What to produce, default is the input item
    """

    def on_input(self, item):
        if self.config["in"] and not self.config["out"]:
            self.put(self.config["what"])
