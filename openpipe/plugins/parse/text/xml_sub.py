"""
# parse text xml_sub

## Purpose
Produce ordered dictionary items from a subset of XML input items

## Trigger
    - Input item is received

## Default
Parse the input item

## Example
```yaml
start:
    - collect from url: https://www.w3schools.com/xml/note.xml
    - parse text xml_sub:
        note:
            body: .
    - pprint:
```
"""

from openpipe.engine import PluginRuntime
from collections import OrderedDict
from pprint import pformat
from sys import stderr
import xmltodict
import json

#  from pprint import pprint
#  from sys import stderr


class Plugin(PluginRuntime):

    def on_input(self, item):
        new_item = self.parse(item, self.config)
        self.put(new_item)

    def extract_xml_dict(self, xml_dict, dict_item):    # NOQA: C901
        current_dict = OrderedDict()
        for key, value in dict_item.items():
            if isinstance(value, str):
                if value == ".":
                    value = key
                try:
                    source_item = xml_dict[key]
                except KeyError:
                    continue
                except TypeError:
                    print("E001 TypeError on XML parsing", file=stderr)
                    print("xml_dict (%s)" % type(xml_dict), file=stderr)
                    print("key=%s" % key, file=stderr)
                    print("xml_dict=%s" % pformat(xml_dict), file=stderr)
                    exit(1)
                current_dict[value] = source_item
            elif isinstance(value, dict):
                for subdict_key, subdict_value in value.items():
                    if subdict_key[0] == "@":
                        current_dict[subdict_value] = xml_dict[key][subdict_key]
                    else:
                        try:
                            sub_dict = xml_dict[key]
                        except KeyError:    # We simply ignore keys which are not found
                            continue
                        except TypeError:
                            print("E002 TypeError on XML parsing", file=stderr)
                            print("xml_dict (%s)" % type(xml_dict), file=stderr)
                            print("key=%s" % key, file=stderr)
                            print("xml_dict=%s" % pformat(xml_dict), file=stderr)
                        sub_result = self.extract_xml_dict(sub_dict, value)
                        current_dict.update(sub_result)
        return current_dict

    def parse(self, xml_input, yaml_input):
        xml_dict = xmltodict.parse(xml_input)

        if not isinstance(yaml_input, dict):
            raise ValueError("ERROR: YAML data must start with a dict")
        extract_result = []
        extract_result = self.extract_xml_dict(xml_dict, yaml_input)
        return json.loads(json.dumps(extract_result))   # Convert OrderedDicts to Dicts
