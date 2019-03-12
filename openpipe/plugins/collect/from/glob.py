"""
Produce list of files matching a glob pattern
"""
from openpipe.engine import PluginRuntime
from glob import glob
from os.path import expanduser


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The path pattern to list
    """

    def on_input(self, item):
        path = self.config
        file_list = glob(expanduser(path))
        if not file_list:
            raise Exception("No file found for " + str(path))
        self.put(file_list)
