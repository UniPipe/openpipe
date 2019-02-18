"""
# collect from clock

## Purpose
Produce the system clock time at regular intervals

## Triggers
    - Input item is received

## Default
Produce the system clock time every second

## Example
```yaml
start:
    - print: Now
    - collect from clock:
        interval: 5s
        max_count: 1
    - print: 5 seconds later...
```
"""
from time import time, sleep
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        start_time = item

        interval = self.config.get('interval', "0")
        interval = time2seconds(interval)
        count = self.config.get('max_count', 0)
        start_wait = self.config.get('start_wait', True)
        repeat_forever = (count == 0)

        if not start_wait:
            self.put(start_time)
            if not repeat_forever:
                count -= 1
        while repeat_forever or count > 0:
            if interval:
                sleep(interval)
            self.put(time())
            if not repeat_forever:
                count -= 1


def time2seconds(value):
    SECONDS_MAP = {'s': 1, 'm': 60, 'h': 60*60, 'd': 24 * 60 * 60}
    number = ''
    unit = 's'
    if isinstance(value, int):
        return value
    for char in value:
        if char.isdigit():
            number += char
        else:
            unit = char
            break
    multiplier = SECONDS_MAP[unit]
    return int(number) * multiplier
