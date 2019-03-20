"""
Write item to a file
"""
from openpipe.pipeline.engine import PluginRuntime
from os.path import expanduser
import json


class Plugin(PluginRuntime):

    required_config = """
    path:                   # Filename of the file to create/overwrite/append
    """

    optional_config = """
    content: $_$            # Content to be written to the file
    mode: "w"               # Open file mode (write/append)
    close_on_item: False    # Force file close after each received item
    """

    def on_start(self, config):
        self.path = config['path']
        self.last_path = None
        self.file = None

    def on_input(self, item):
        path = self.config['path']
        path = expanduser(path)
        if path != self.last_path:
            if self.file:
                self.file.close()
            self.file = open(path, self.config['mode'])
            self.last_path = path
        content = self.config['content']
        if path.endswith('.json'):
            content = json.dumps(content, indent=4)
        self.file.write(content)
        if self.config['close_on_item']:
            self.file.close()
            self.file = None
            self.last_path = None
        self.put(item)

    def on_finish(self, reason):
        if self.file:
            self.file.close()
