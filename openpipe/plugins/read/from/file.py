"""
Produce metadata/content from a local or remote file
"""
import gzip
import bz2
import lzma
import zlib
import mimetypes
import urllib.request as urlreq
from re import findall
from urllib.error import HTTPError
from io import BytesIO, StringIO
from os.path import splitext, expanduser
from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    path:                       # Local path or HTTP/HTTPS/FTP url
    """

    optional_config = """
    # The mime_type will be used by the plugin to identify and automatically
    # decode the file content.
    # With the default value of 'auto' the action will try to guess the
    # mime type based on the content header or file extension.
    mime_type:  auto

    # Possible values are: "meta", "content" or "both"
    output_type: auto

    # The following option is only applicable to local filenames
    auto_expand_home: True      # Expand '~' on path to user home dir

    # The following options are only relevant for HTTP/HTTPS/FTP paths
    timeout: 30                 # Global timeout (in secs) for the operation
    ignore_http_errors: False   # Ignore HTTP errors replies
    user_agent: curl/7.64.0     # User-agent to use on HTTP requests
    """

    """
    This plugin can be extended with mime type decoders, on start it will load
    modules available from the _file directory. Those modules must attach
    a file handler using the class method `attach_file_handler` .
    """
    MIME_FILE_HANDLER = {}
    EXTENSION_FILE_HANDLER = {}

    @classmethod
    def attach_file_handler(cls, decoder_function, mime_type=None, file_extension=None):
        if mime_type:
            cls.MIME_FILE_HANDLER[mime_type] = decoder_function
        if file_extension:
            cls.EXTENSION_FILE_HANDLER[file_extension] = decoder_function

    def on_start(self, config):
        self.extend(__file__, "_file")

    def on_input(self, item):
        path = self.config["path"]
        schema = path.split(":", 1)[0]
        is_remote = ":" in path and schema in ["http", "https", "ftp"]
        mime_type = mimetypes.guess_type(path)[0]
        if is_remote:
            self.collect_remote_file(path, mime_type)
        else:
            self.collect_local_file(path, mime_type)

    def collect_local_file(self, path, mime_type):

        ext_map = {
            ".gz": lambda x: gzip.open(x, "r"),
            ".bz2": lambda x: bz2.open(x, "r"),
            ".xz": lambda x: lzma.open(x, "r"),
            "*": lambda x: open(x, "rb"),
        }

        if self.config["auto_expand_home"]:
            path = expanduser(path)

        filename, file_extension = splitext(path)

        open_func = ext_map.get(file_extension, ext_map["*"])

        # If it's a compressed file, split the filename again
        if file_extension in ext_map:
            filename, file_extension = splitext(filename)
            mime_type = mimetypes.guess_type(path)[0]

        with open_func(path) as file:

            # mime type can be overridden from the action config
            if self.config["mime_type"] != "auto":
                mime_type = self.config["mime_type"]
            self.decode(file, mime_type)

    def collect_remote_file(self, path, mime_type):

        ext_map = {
            ".gz": lambda x: zlib.decompress(x, 16 + zlib.MAX_WBITS),
            ".xz": lambda x: lzma.decompress(x),
            ".bz2": lambda x: bz2.decompress(x),
        }
        url = path
        req = urlreq.Request(url)
        req.add_header("User-Agent", self.config["user_agent"])
        try:
            reply = urlreq.urlopen(req, timeout=self.config["timeout"])
        except HTTPError:
            if self.config["ignore_http_errors"]:
                return
            raise
        file_data = reply.read()
        filename, file_extension = splitext(url)
        mime_type, mime_extension = mimetypes.guess_type(path)
        encoding = None
        try:
            content_type = reply.getheader("Content-Type")
        except AttributeError:  # FTP does not have a getheader
            pass
        else:
            # Only use header mime type when mime type was not determined by extension
            if not mime_type:
                mime_type = content_type.split(';', 1)[0]
            charset = findall(r'charset=(\S*)', content_type)
            if charset:
                encoding = charset[0]

        decompress_func = ext_map.get(file_extension)
        if decompress_func:
            file_data = decompress_func(file_data)
            # If we got a gz file, guess the mime type from the remaining extension
            filename, file_extension = splitext(filename)
            mime_type = mimetypes.guess_type(path)[0]
        if encoding:
            file_data = file_data.decode(encoding)
            file = StringIO(file_data)
        else:
            file = BytesIO(file_data)
        self.decode(file, mime_type)

    def decode(self, fileobj, mime_type):
        decoder_function = self.MIME_FILE_HANDLER.get(mime_type)
        if decoder_function:
            decoder_function(fileobj, self)
        else:
            data = fileobj.read()
            self.put(data)
