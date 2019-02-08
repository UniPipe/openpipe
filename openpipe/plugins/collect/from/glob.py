""" Example
## Purpose
Produce the list of files matching a glob pattern

## Trigger
    - Input item is received

## Example:
```yaml
    start:
        - collect from glob: /tmp/*
        - pprint:
```

## Related Documentation
    - https://docs.python.org/3/library/glob.html#module-glob

"""
from openpipe.engine import PluginRuntime
from glob import glob
from os.path import expanduser


class Plugin(PluginRuntime):

    __default_config__ = "$_$"

    def on_input(self, item):
        path = self.config
        file_list = glob(expanduser(path))
        if not file_list:
            raise Exception("No file found for " + str(path))
        self.put(file_list)
