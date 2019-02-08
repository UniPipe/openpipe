"""
# insert

## Purpose
Insert an item in the output stream

## Trigger
    - Input item is received

## Example
```yaml
start:
    - insert:
        name: John
        message: This will create a new dict item
    - pprint:   # Output: {'message': 'This will create a new dict item', 'name': 'John'}
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    # Output the configuration item
    def on_input(self, item):
        if isinstance(self.config, str):
            self.put(self.config)
            #  for line in self.config.splitlines():
            #      self.put(line)
        elif isinstance(self.config, list):
            for list_item in self.config:
                self.put(list_item)
        else:
            self.put(self.config)
