"""
Produce metadata/content from an URL
"""
import bz2
import lzma
import zlib
import mimetypes
import urllib.request as urlreq
from io import BytesIO, StringIO
from re import findall
from urllib.error import HTTPError
from openpipe.pipeline.engine import ActionRuntime
from os.path import splitext
from .file_ import Action as FileAction


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_config = """
    url:                       # HTTP/HTTPS/FTP url
    """

    optional_config = """
    # The mime_type will be used by the action to identify and automatically
    # decode the file content.
    # With the default value of 'auto' the action will try to guess the
    # mime type based on the content header or file extension.
    mime_type:  auto

    # The following options are only relevant for HTTP/HTTPS/FTP paths
    timeout: 30                 # Global timeout (in secs) for the operation
    ignore_http_errors: False   # Ignore HTTP errors replies
    user_agent: curl/7.64.0     # User-agent to use on HTTP requests
    """

    def on_start(self, config):
        self.extend(__file__, "_file")
        self.file_action = FileAction(self.action_label, None)
        self.file_action.extend(__file__, "_file")

    def on_input(self, item):
        url = self.config["url"]
        mime_type = mimetypes.guess_type(url)[0]
        ext_map = {
            ".gz": lambda x: zlib.decompress(x, 16 + zlib.MAX_WBITS),
            ".xz": lambda x: lzma.decompress(x),
            ".bz2": lambda x: bz2.decompress(x),
        }
        req = urlreq.Request(url)
        req.add_header("User-Agent", self.config["user_agent"])
        try:
            reply = urlreq.urlopen(req, timeout=self.config["timeout"])
        except HTTPError:
            if self.config["ignore_http_errors"]:
                return
            raise
        file_data = reply.read()
        mime_type = mimetypes.guess_type(url)[0]
        encoding = None
        try:
            content_type = reply.getheader("Content-Type")
        except AttributeError:  # FTP does not have a getheader
            pass
        else:
            # Only use header mime type when mime type was not determined by extension
            if not mime_type:
                mime_type = content_type.split(";", 1)[0]
            charset = findall(r"charset=(\S*)", content_type)
            if charset:
                encoding = charset[0]

        filename, file_extension = splitext(url)
        decompress_func = ext_map.get(file_extension)
        if decompress_func:
            file_data = decompress_func(file_data)
            # If we got a gz file, guess the mime type from the remaining extension
            filename, file_extension = splitext(filename)
            mime_type = mimetypes.guess_type(url)[0]
        if encoding:
            file_data = file_data.decode(encoding)
            file = StringIO(file_data)
        else:
            file = BytesIO(file_data)

        forced_mime_type = self.config.get("mime_type")
        if forced_mime_type != "auto":
            mime_type = forced_mime_type

        self.file_action.decode(file, mime_type, self)
