"""
# copy to segment

## Purpose
Copy the input item into one or more segments

## Trigger
    - Input item is received

## Example
```yaml
start:
    - insert: ok
    - copy to segment:
        - seg1
        - seg2
    - print: Start segment
seg1:
    - print: Segment one
seg2:
    - print: Segment two
"""

from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        self.put(item)
