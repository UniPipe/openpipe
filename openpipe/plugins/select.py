"""
# select

## Purpose
Select input items matching a search condition

## Trigger
    - Input item is received

## Default
Print the input item

## Example
```yaml
start:
    - insert:   # Inserting a list, each item will be sent individually
        - "Hello World"
        - "Good morning"
        - "No Hello!"
    - select: $ "Hello" in _  $     # _ is an alias for the entire input item
    - print:
```
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        if isinstance(self.config, bool):
            if self.config is True:
                self.put(item)
        else:
            if self.config:
                self.put(self.config)
