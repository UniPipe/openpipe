"""
# check file existence

## Purpose
Send content depending on file existence

## Trigger
    - Input item is received

## Configuration
    - [path: $_$]       - Filename to be checked
    - [content: $_$]    - Filename to be checked
    - [output_on: True] - When to output the content

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
        "output_if": True
    }

    def on_input(self, item):
        check_condition = exists(self.config['path'])
        if not self.config['output_if']:
            check_condition = not check_condition
        if check_condition:
            self.put(self.config['content'])
