"""
# pprint

## Purpose
Pretty print a configuration item

## Trigger
    - Input item is received

## Default
Pretty print the input item

## Example
```yaml
start:
    - pprint: Hello word!
```
"""

from openpipe.engine import PluginRuntime
from pprint import pprint


class Plugin(PluginRuntime):

    __default_config__ = "$_$"  # The default behavior is to print the input item

    def on_input(self, item):
        pprint(self.config)
        self.put(item)
