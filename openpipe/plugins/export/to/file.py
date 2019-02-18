"""
# export to file

## Purpose
Export content to file

## Trigger
    - Input item is received
    - Input ends

## Configuration
    - path:                     - Filename of the file to be created/overwritted/appended
    - [content: $_$]            - Content to be written to the file
    - [mode: "w"]               - Open file mode (write/append)
    - [on_item_close: False]    - Force file close after each received item

## Example
```yaml
start:
    - export to file:
        path: /tmp/test
        content: Hello World!
```
"""
from openpipe.engine import PluginRuntime
from os.path import expanduser
import json


class Plugin(PluginRuntime):

    __default_config__ = {
        "mode": "w",
        "content": "$_$",
        "close_on_item": False
    }

    def on_start(self, config, segment_resolver):
        self.last_path = None
        self.file = None

    def on_input(self, item):
        if isinstance(self.config, str):
            path = self.config
        else:
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

    def on_complete(self):
        if self.file:
            self.file.close()
