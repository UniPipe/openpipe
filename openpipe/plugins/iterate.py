"""
# iterate

## Purpose
Procude items by iterating over the content of a field

## Trigger
    - Input item is received

## Configuration
    Simple: name of the input field to be iterated

## Example
```yaml
start:
    - insert:
        size: 12
        color: [red, blue, brown]
    - iterate: color
    - print: $_$
```
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        original_iterator = item[self.config]
        for iter_item in original_iterator:
            item[self.config] = iter_item
            self.put(item)
