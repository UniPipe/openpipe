# Openpipe Action Plugin Development
This document provides is a quick reference for developers planning to write openpipe  plugins.


### Example Plugin Code
```python
"""
Print content to the standard output
"""
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The content to be printed, default is the input item ($_$)
    """

    def on_input(self, item):
        print(self.config)      # Print item to the console
        self.put(item)          # No change to the data stream, input -> output
```

### Example Plugin Usage
```yaml
start:
    print: Hello world
```

## Introduction
An openpipe plugin is a regular Python module with the following requirements:

- Must provide a docstring with a short description, the first line will be displayed on _openpipe help_
- Must provide a class named `Plugin`, which:
    - Must be derived from the `PluginRuntime` class
    - May provide the following class attributes to be handled by the pipeline engine:
        - `required_config`: string with YAML describing required parameters
        - `optional_config`: string with YAML describing optional parameters
    - May provide the following class methods to be invoked by the pipeline engine:
        - `on_start(self, config)`: invoked when the pipeline is started
        - `on_input(self, item)`: invoked when an input item is received
            - may use `self.put(item)` once or multiple times to produce items
        - `on_finish(self, reason)`: invoked when the pipeline is finished