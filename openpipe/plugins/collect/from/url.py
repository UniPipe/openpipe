"""
# collect from url

## Purpose
Retrieve a file from an HTTP/HTTPS URL

## Trigger
    - Input item is received


## Example
```yaml
start:
    # Check for changes every 5s
    - collect from url:
        url: https://raw.githubusercontent.com/OpenPipe/openpipe/master/LICENSE
    - pprint:
```
"""

from openpipe.engine import PluginRuntime
import urllib.request as urlreq
from urllib.error import HTTPError


def lower(some_dict):
    new_dict = {}
    for key, value in some_dict.items():
        key = key.lower()
        new_dict[key] = value
    return new_dict


class Plugin(PluginRuntime):

    __default_config__ = {
        "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",  # NOQA: E501
        "timeout": 30,
        "path": "$_$",
        "content_only": True,
        "split_lines": True,
        }

    def on_input(self, item):
        if isinstance(self.config, str):
            url = self.config
            self.config = self.__default_config__
        else:
            url = self.config['url']
        timeout = self.config['timeout']
        req = urlreq.Request(url)
        req.add_header('User-Agent', self.config['ua'])
        try:
            reply = urlreq.urlopen(req, timeout=timeout)
        except HTTPError:
            if self.config.get('ignore_errors', False):
                return
            raise
        use_splitlines = self.config['split_lines']
        if url.split('.')[-1] in ['json', 'xml']:
            use_splitlines = False
        content_data = reply.read().decode('utf-8')
        if use_splitlines:
            content_data = content_data.splitlines()
        if self.config['content_only']:
            if use_splitlines:
                for line in content_data:
                    self.put(line)
            else:
                self.put(content_data)
        else:
            new_item = {}
            new_item['info'] = lower(dict(reply.info()))
            new_item['code'] = reply.getcode()
            new_item['url'] = url = reply.geturl()
            new_item['content'] = content_data
            self.put(new_item)
