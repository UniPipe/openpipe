"""
# check file existence

## Purpose
Send content depending on file existence

## Trigger
    - Input item is received

## Configuration
    - [path: $_$]       - Filename to be checked
    - [content: $_$]    - Filename to be checked
    - [send if: True]   - When to send content

## Example
```yaml
start:
    - check file existence:
        path: /etc/hosts
    - print: File $_$ was found
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = {
        "path": "$_$",
        "content": "$_$",
        "send if": True
    }

    def on_input(self, item):
        pass
