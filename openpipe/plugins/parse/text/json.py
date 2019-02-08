"""
# parse text json

## Purpose
Produce dictionary items from JSON input items

## Trigger
    - Input item is received

## Default
Parse the input item

## Example
```yaml
start:
    - collect from url:
        url: https://api.github.com/gists
        only_content_lines: False
    - parse text json: $content$
    - pprint:
```
"""
from json import loads
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = "$_$"

    def on_input(self, item):
        new_item = loads(item)
        self.put(new_item)
