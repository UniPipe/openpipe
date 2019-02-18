"""
# parse line split

## Purpose
Produce dictionary items by using split on line based input items

## Trigger
    - Input item is received

## Example
```yaml
start:
    - collect from file: /etc/passwd
    - parse line split:
        sep: ':'
        field_list: [username, password, uid, gid, gecos, home, shell]
    - pprint:
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = {
        "sep": ",",
        "maxsplit": -1,
        "auto_number": True,
        }

    def on_start(self, config, segment_resolver):
        self.sep = config['sep']
        self.maxsplit = config['maxsplit']
        self.field_list = config.get('field_list', None)

        if self.field_list:
            self.expected_len = len(self.field_list)
            self.on_input = self.on_input_field_list

    # Output the configuration item
    def on_input(self, item):
        columns = item.split(self.sep)
        self.put(columns)

    def on_input_field_list(self, item):
        parts = item.split(self.sep)
        item_len = len(parts)
        if self.expected_len != item_len:
            raise ValueError("Expected {} field(s), got {}".format(self.expected_len, item_len))
        new_item = {}

        for i, part_name in enumerate(self.field_list):
            new_item[part_name] = parts[i]

        if self.config['auto_number']:
            for i, part_name in enumerate(self.field_list):
                try:
                    new_item[part_name] = int(parts[i])
                except ValueError:
                    try:
                        new_item[part_name] = float(parts[i])
                    except ValueError:
                        pass

        self.put(new_item)
