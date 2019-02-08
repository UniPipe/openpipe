"""
# print

## Purpose
Print an item

## Trigger
    - Input item is received

## Default
Print the input item

## Example
```yaml
start:
    - insert: This is an input item
    - print:    # Output: This is an input item
    - print: Reached end of first block     # Output: Reached end of first block
    - insert: { size: 12, color: "red" }
    - print: The color is $color$   # Output: The color is red
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    # The default behavior is to print the input item
    __default_config__ = "$_$"

    def on_input(self, item):
        if isinstance(self.config, dict):
            for key, value in self.config.items():
                print("%s: %s" % (key, value))
        else:
            print(self.config)
        self.put(item)
