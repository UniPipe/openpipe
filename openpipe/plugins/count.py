"""
# count

## Purpose
Produce the count of input elements

## Trigger
    - Input item is received

## Example
```yaml
start:
    - insert:
        - abc
        - xyz
    - print:
```
"""


from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = None

    def on_start(self, config, segment_resolver):
        self.count = 0

    def on_input(self, item):
        self.count += 1
        if self.config:
            new_item = item.copy()
            new_item[self.to_field] = self.count
            self.put(new_item)
        else:
            self.put(self.count)
