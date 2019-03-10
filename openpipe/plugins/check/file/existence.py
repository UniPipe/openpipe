"""
# check file existence

## Purpose
Produces content depending on file existence

## Trigger
    - Input item is received

## Configuration
    - [path: $_$]       - Filename to be checked
    - [content: $_$]    - Content to be produced
    - [output on: True] - When to output the content

## Example
```yaml
start:
    - check file existence:
        path: /etc/hosts
    - print: File $_$ was found
```
"""
from openpipe.engine import PluginRuntime
from os.path import exists


class Plugin(PluginRuntime):

    __default_config__ = {
        "path": "$_$",
        "content": "$_$",
        "output on": True
    }

    def on_input(self, item):
        check_condition = exists(self.config['path'])
        if not self.config['output on']:
            check_condition = not check_condition
        if check_condition:
            self.put(self.config['content'])
