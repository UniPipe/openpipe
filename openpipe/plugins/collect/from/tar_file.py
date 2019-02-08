"""
# collect from tar_file

## Purpose
Retrieve files from a TAR archive

## Trigger
    - Input item is received

## Example
```yaml
start:
    - collect from tar_file: samples/test.tar
    - print: $name$
```
"""

from openpipe.engine import PluginRuntime
import tarfile


class Plugin(PluginRuntime):

    __default_config__ = "$_$"

    def on_input(self, item):
        filename = self.config
        with tarfile.open(filename) as tar:
            while True:
                file_info = tar.next()
                if file_info is None:   # Reached end of archive
                    break
                if not file_info.isfile():
                    continue
                single_file = tar.extractfile(file_info)
                new_item = {}
                new_item['name'] = file_info.name
                new_item['content'] = single_file.read()
                single_file.close()
                self.put(new_item)
