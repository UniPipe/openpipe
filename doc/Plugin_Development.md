# OpenPipe Plugin Development
This document provides is a quick reference for developers planning to write openpipe plugins.

## Introduction
An openpipe plugin is a regular Python module, with the following specific requirements:

- Must provide a docstring, the first line will be displayed on `openpipe help`
- It must provide a class named `Plugin` meeting the following requirements:
    - must be derived from the `PluginRuntime` class
    - may contain the following class attributes:
        - `required_config`: string with YAML describing required config parameters
        - `optional_config`: string with YAML describing optional config parameters
    - the following optional methods will be invoked during pipeline execution:
        - `on_start(self, config)`: invoked when the pipeline is started
        - `on_input(self, item)`: invoked when an input item is received
            - may use `self.put(item)` once or multiple times to produce items
        - `on_finish(self, reason)`: invoked when the pipeline is finished

### Example Code
```python
"""
Print content
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The content to be printed, default is the input item ($_$)
    """

    def on_input(self, item):
        print(self.config)      # Print item to the console
        self.put(item)          # No change to the data stream, input -> output
```

### Example Usage
```yaml
start:
    print: Hello world
```