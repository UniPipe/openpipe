"""
Produce the system clock time at regular intervals
"""
from time import time, sleep, strftime
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    optional_config = """
    interval:   0     # Pause time between insertions
    max_count:  1     # Max number of item insertions, 0 means forever
    format:     ""    # Time output format (strftime)
    """

    category = "Data Sourcing"

    def on_input(self, item):
        interval = self.config["interval"]
        interval = time2seconds(interval)
        count = self.config["max_count"]
        repeat_forever = count == 0
        str_format = self.config["format"]

        while repeat_forever or count > 0:
            if interval:
                sleep(interval)
            if str_format == "":
                new_item = time()
            else:
                new_item = strftime(str_format)
            self.put(new_item)
            if not repeat_forever:
                count -= 1


def time2seconds(value):
    SECONDS_MAP = {"s": 1, "m": 60, "h": 60 * 60, "d": 24 * 60 * 60}
    number = ""
    unit = "s"
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
