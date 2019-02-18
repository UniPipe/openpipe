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

    def on_start(self, config, segment_resolver):
        self.copy_targets = copy_targets = []
        for item in config:
            segment_start = segment_resolver(item)
            copy_targets.append(segment_start)

    def on_input(self, item):
        for target in self.copy_targets:
            self.put_target(item, target)
        self.put(item)
