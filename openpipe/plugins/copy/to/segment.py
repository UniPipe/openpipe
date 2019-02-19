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
        self.target_segmment = segment_resolver(config)

    def on_input(self, item):
        self.put_target(item, self.target_segmment)
        self.put(item)

    def on_complete(self):
        self.put_target(None, self.target_segmment)
