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

    __default_config__ = "{}"

    def on_start(self, config, segment_resolver):
        self.count = 0
        self.to_field = None

    def on_input(self, item):
        if isinstance(self.config, dict):
            self.to_field = self.config.get("to_field", None)

        self.count += 1
        if self.to_field:
            item[self.to_field] = self.count
            self.put(item)
        else:
            self.put(self.count)
