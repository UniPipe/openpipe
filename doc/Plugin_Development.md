# OpenPipe Plugin Development
This document provides is a quick reference for developers planning to write openpipe plugins.

## Introduction
An openpipe plugin is a regular Python module with the following structure:

- Must provide a docstring with a short description, the first line will be displayed on _openpipe help_
- Must provide a class named `Plugin`, which:
    - Must be derived from the `PluginRuntime` class
    - May provide the following class attributes to be handled by the pipeline engine:
        - `required_config`: string with YAML describing required config parameters
        - `optional_config`: string with YAML describing optional config parameters
    - May provide the following class methods to be invoked by the pipeline engine:
        - `on_start(self, config)`: invoked when the pipeline is started
        - `on_input(self, item)`: invoked when an input item is received
            - may use `self.put(item)` once or multiple times to produce items
        - `on_finish(self, reason)`: invoked when the pipeline is finished

### Example Plugin Code
```python
"""
Print content to the standard output
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

### Example Plugin Usage
```yaml
start:
    print: Hello world
```

## Plugin Configuration Schema

A plugin can have required and optional configuration options. The plugin configuration schema is defined by the `required_config` and `optional_config` class attributes as described in this section.

The `required_config` when provided sets the following rules:
- must be a string containing valid YAML
- the YAML must be a _dict_
- all the _dict_ values must be set to _None_
- the _config_ attribute available to the plugin methods will be a _dict_
- if the user provided config is a _dict_:
    - all `required_config` keys must be present
- else:
    - if `required_config` contains a single key:
        - _config[required_key]_ will be set to the user provided config value
        - Set user provided config to _None_
    - else:
        - reports configuration format error

The `optional_config` when provided sets the following rules:
- must be a string containing valid YAML
- if `required_config` was provided:
    - `optional_config` YAML must be a _dict_
- if `optional_config` is a _dict_:
    - update _config_ with `required_config`
    - update _config_ with the user provided config
- if `optional_config` is _not a dict_:
    - if user provided config is None:
        - Set _config_ to user `optional_config`
    - else:
        - Set _config_ to user provided config

If `required_config` is _dict_ or `optional_config` is _dict_ and user provided config is _dict_, report unknown keys presented on user provided config.