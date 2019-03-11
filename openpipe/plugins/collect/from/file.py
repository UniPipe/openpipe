"""
Produce content of a file
"""
import gzip
import bz2
from openpipe.engine import PluginRuntime
from os.path import splitext, expanduser


class Plugin(PluginRuntime):

    default_config = """
    path: $_$               # Path of the file to be produced

    # If a single string item is provided, it will be used as the path

    split_lines: True     # Produce content line-by-line
    """

    ext_map = {
        '.gz': lambda x: gzip.open(x, 'r'),
        '.bz': lambda x: bz2.open(x, 'r'),
        '*': lambda x: open(x),
        }

    def on_input(self, item):
        if isinstance(self.config, str):
            path = self.config
            split_lines = True
        else:
            path = self.config['path']
            split_lines = self.config.get('split_lines')
        path = expanduser(path)
        filename, file_extension = splitext(path)

        if file_extension in ['.json', '.yaml', '.xml']:
            split_lines = False

        open_func = self.ext_map.get(file_extension, self.ext_map['*'])
        with open_func(path) as file:
            if split_lines:
                for line in file:
                    line = line.strip("\r\n")
                    self.put(line)
            else:
                data = file.read()
                self.put(data)
