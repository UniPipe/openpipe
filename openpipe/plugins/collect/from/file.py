"""
Insert metadata/content from local or remote file
"""
import gzip
import bz2
import zlib
import urllib.request as urlreq
import xmltodict
from urllib.error import HTTPError
from os.path import splitext, expanduser
from json import loads
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    path:                       # Local path or HTTP/HTTPS/FTP url
    """

    optional_config = """
    content_only: True          # Insert only the content
    split_lines: True           # Insert line by line (enforces content_only)
    auto_decompress: True       # Automatically decompress .gz/.bz files
    auto_parse: True            # Automatically parse json/xml files

    # The following option is only relevant for local files
    auto_expand_home: True      # Expand '~' on path to user home dir

    # The following options are only relevant for HTTP(S) paths
    timeout: 30                 # Maximum time (in seconds) allowed for the operation
    ignore_http_errors: False   # Ignore HTTP errors replies
    user-agent: curl/7.64.0     # User-agent to use on HTTP requests
    """

    results = """
    """

    def on_input(self, item):
        path = self.config['path']
        schema = path.split(':', 1)[0]
        is_remote = ':' in path and schema in ['http', 'https', 'ftp']

        if is_remote:
            self.collect_remote_file()
        else:
            self.collect_local_file()

    def put_or_parse(self, data, file_extension):
        auto_parse_map = {
            '.json': lambda x: loads(x),
            '.xml': lambda x: xmltodict.parse(x),
            '*': lambda x: x,
            }
        if not self.config['auto_parse']:
            self.put(data)
            return
        parse_function = auto_parse_map.get(file_extension)
        if parse_function:
            self.put(parse_function(data))
        else:
            self.put(data)

    def collect_local_file(self):
        ext_map = {
            '.gz': lambda x: gzip.open(x, 'r'),
            '.bz': lambda x: bz2.open(x, 'r'),
            '*': lambda x: open(x),
            }
        path = self.config['path']
        split_lines = self.config['split_lines']

        if self.config['auto_expand_home']:
            path = expanduser(path)

        filename, file_extension = splitext(path)
        open_func = ext_map.get(file_extension, ext_map['*'])

        # If it's a compressed file, split the filename
        if file_extension in ext_map:
            filename, file_extension = splitext(filename)

        if file_extension in ['.json', '.yaml', '.xml']:
            split_lines = False

        with open_func(path) as file:
            if split_lines:
                for line in file:
                    line = line.strip("\r\n")
                    self.put(line)
            else:
                data = file.read()
                self.put_or_parse(data, file_extension)

    def collect_remote_file(self):
        url = self.config['path']
        req = urlreq.Request(url)
        req.add_header('User-Agent', self.config['user-agent'])
        try:
            reply = urlreq.urlopen(req, timeout=self.config['timeout'])
        except HTTPError:
            if self.config['ignore_http_errors']:
                return
            raise
        content_raw = reply.read()
        filename, file_extension = splitext(url)
        if hasattr(reply, "getheader"):  # FTPs do not provide headers
            content_type = reply.getheader('Content-Type').split(';', 1)[0]
            if content_type == 'application/x-gzip':
                content_raw = zlib.decompress(content_raw, 16+zlib.MAX_WBITS)
            if content_type == 'application/json':
                file_extension = '.json'
        if file_extension == '.json':
            content_raw = content_raw.decode('utf-8')
        self.put_or_parse(content_raw, file_extension)
