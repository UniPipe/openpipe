"""
Produce content depending on file existence
"""
from openpipe.engine import PluginRuntime
from os.path import exists


class Plugin(PluginRuntime):

    default_config = """
    path: $_$         # Path of the file to be checked
    content: $_$      # Content to be produced
    output on: True   # When to output the content
    """

    def on_input(self, item):
        check_condition = exists(self.config['path'])
        if not self.config['output on']:
            check_condition = not check_condition
        if check_condition:
            self.put(self.config['content'])
