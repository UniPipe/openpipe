"""
# collect from file

## Purpose
Produce the content of a file

## Trigger
    - Input item is received

## Default
Use input item for the path filename

## Example
```yaml
start:
    # Print each line from /etc/hosts prefixed with '>'
    - collect from file:
        path: /etc/hosts
    - print: "> $_$"
```
"""
import gzip
import bz2
from openpipe.engine import PluginRuntime
from os.path import splitext, expanduser


class Plugin(PluginRuntime):

    __default_config__ = "$_$"

    ext_map = {
        '.gz': lambda x: gzip.open(x, 'rt'),
        '.bz': lambda x: bz2.open(x, 'rt'),
        '*': lambda x: open(x),
        }

    def on_input(self, item):
        full_content = False
        if isinstance(self.config, str):
            path = self.config
        else:
            path = self.config['path']
            full_content = self.config.get('full_content', False)
        path = expanduser(path)
        filename, file_extension = splitext(path)

        if file_extension in ['.json', '.yaml']:
            full_content = True

        open_func = self.ext_map.get(file_extension, self.ext_map['*'])
        with open_func(path) as file:
            if full_content:
                data = file.read()
                self.put(data)
            else:
                for line in file:
                    line = line.strip("\r\n")
                    self.put(line)
