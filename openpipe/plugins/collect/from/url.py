"""
Produce properties and content of a file obtained from an HTTP/HTTPS URL
"""

from openpipe.engine import PluginRuntime
import urllib.request as urlreq
from urllib.error import HTTPError
from os.path import splitext
import zlib


class Plugin(PluginRuntime):

    optional_config = """
    path: $_$           # Local path or HTTP,HTTPS,FTP url

    # If a single string item is provided, it will be used as the path

    content_only: True  # Produce the content only
    split_lines: True  # Produce content line-by-line
    timeout: 30,        # Maximum time (in seconds) allowed for the operation
    ua: curl/7.64.0     # User-agent to use on requests

    """

    def on_start(self, config):
        self.path = self.config if isinstance(self.config, str) else None

    def on_input(self, item):
        url = self.url or self.config['url']
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
        filename, file_extension = splitext(url)
        content_raw = reply.read()
        if file_extension == '.gz':
            content_raw = zlib.decompress(content_raw, 16+zlib.MAX_WBITS)
            filename, file_extension = splitext(filename)
        if file_extension in ['.json', '.xml', '.tar']:
            use_splitlines = False
        content_type = reply.getheader('Content-Type')
        if 'application/json' in content_type:
            use_splitlines = False
        if file_extension in ['.json', '.xml']:
            content_data = content_raw.decode('utf-8')
        else:
            content_data = content_raw
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


def lower(some_dict):
    new_dict = {}
    for key, value in some_dict.items():
        key = key.lower()
        new_dict[key] = value
    return new_dict
