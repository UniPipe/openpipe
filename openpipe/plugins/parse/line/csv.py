"""
# parse line csv

## Purpose
Produce dictionary from CSV line based input data

## Trigger
    - Input item is received

## Example
```yaml
start:
    - collect from url:
        https://raw.githubusercontent.com/openmundi/world.csv/master/countries(249)_alpha2.csv
    - parse line csv:
    - pprint:
```
"""
import sys
import csv
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = {
        "delimiter": ",",
        "quotechar": '"',
        "auto_number": True,
        "ignore_errors": False,
        }

    def on_start(self, config, segment_resolver):
        self.mapper = None

    def on_input(self, item):

        # Some CSV files provide a trailing new line
        item = item.strip()
        if item == '':
            return

        if self.mapper is None:
            ignore_errors = self.config['ignore_errors']
            item_field_list = item.split(self.config['delimiter'])
            # Strip surrounding spaces
            item_field_list = [x.strip(" ") for x in item_field_list]
            # Strip quote chars
            item_field_list = [x.strip(self.config['quotechar']) for x in item_field_list]
            field_list = self.config.get('field_list', item_field_list)
            self.mapper = CSVMapper(
                field_list,
                self.config['delimiter'],
                self.config['quotechar'],
                ignore_errors=ignore_errors
            )

            # If no field list was provided, first line is just the header, do nothing
            if not self.config.get('field_list'):
                return

        new_item = self.mapper.parse(item)
        if new_item:
            self.put(new_item)


class CSVMapper:

    def __init__(self, field_list, delimiter=',', quotechar='"', ignore_errors=False):
        self.delimiter, self.quotechar = delimiter, quotechar
        self.build_field_groups(field_list)
        self.ignore_errors = ignore_errors

    def build_field_groups(self, field_list):
        """
        Create a field group for each item in the list, when ":count" is not provided, use 1
        A field group is a tuple (field_name, field_count), csv values will be mapped to fields
        based in the field group definition
        """
        self.field_list = []
        self.field_count = 0

        for counter, value in enumerate(field_list):
            if ':' in value:
                field_name, field_count = value.split(':')
                field_count = int(field_count)
            else:
                field_name, field_count = value, 1
            field_name = field_name.strip()
            field_group = field_name, field_count
            self.field_list.append(field_group)
            self.field_count += field_count

    def parse(self, line):
        reader = csv.reader([line], delimiter=self.delimiter, quotechar=self.quotechar)
        row = [x for x in reader][0]
        if self.field_count != len(row):
            if self.ignore_errors:
                return
            print("FIELD_LIST",  self.field_list, file=sys.stderr)
            raise Exception("Expected %d elements, got %d" % (self.field_count, len(row)))
        new_item = {}
        field_index = 0
        for field_group in self.field_list:
            field_name, field_count = field_group
            if field_name[0] != '~':
                if field_name[0] == '%':
                    field_name = field_name[1:]
                    new_item[field_name] = int(row[field_index])
                else:
                    field_group = row[field_index:field_index+field_count]
                    new_item[field_name] = self.delimiter.join(field_group)
            field_index += field_count
        return new_item
