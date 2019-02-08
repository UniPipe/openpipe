"""
# join

## Purpose
Extend input item with config item

## Trigger
    - Input item is received

## Example 1
```yaml
start:
    - insert:
        name: Tono
    - join:
        - { age: 14 }
    - pprint:   # Output: {'age': 14, 'name': 'Tono'}
```
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    # Output the configuration item
    def on_input(self, item):
        for extend_item in self.config:
            new_item = {**item, **extend_item}
            self.put(new_item)
