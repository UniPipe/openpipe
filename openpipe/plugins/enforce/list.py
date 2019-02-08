"""
# enforce list

## Purpose
If input part is not a list, transform it into a single item list

## Trigger
    - Input item is received

## Example
```yaml
start:
    - insert:
        { name: ok }
    - enforce list:
            name
    - pprint:   # Output: {'name': ['ok']}
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        key_name = self.config
        key_item = item[key_name]
        if not isinstance(key_item, list):
            item[key_name] = [key_item]
        self.put(item)
