"""
# parse text xml

## Purpose
Produce ordered dictionary items from XML input items

## Trigger
    - Input item is received

## Default
Parse the input item

## Example
```yaml
start:
    - collect from url:
        url: https://www.w3schools.com/xml/note.xml
        only_content_lines: False
    - parse text xml: $content$
    - pprint:
```
"""
import xmltodict
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    __default_config__ = "$_$"

    def on_input(self, item):
        self.put(xmltodict.parse(self.config))
