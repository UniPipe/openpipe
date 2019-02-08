"""
# collect from ftp

## Purpose
Retrieve a file from a FTP server

## Trigger
    - Input item is received


## Example
```yaml
start:
    # Check for changes every 5s
    - collect from ftp:
        source: ftp://ftp.hosteurope.de/pub/linux/debian/README
        destination: ftp.txt
    - print: "File was downloaded to $_$"```
"""
from openpipe.engine import PluginRuntime
from urllib.request import urlretrieve


class Plugin(PluginRuntime):

    def on_input(self, item):
        source = self.config['source']
        destination = self.config['destination']
        urlretrieve(source, destination)
        self.put(destination)
