"""
Create and change to directory
"""
from os import makedirs, chdir, getcwd
from os.path import exists
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
        path:    # Name of the directory to create (if not found) and change to
    """

    def on_input(self, item):
        self.cwd = getcwd()
        dir_name = self.config['path']
        if not exists(dir_name):
            makedirs(dir_name)
        chdir(dir_name)
        self.put(item)

    def on_complete(self):
        chdir(self.cwd)
