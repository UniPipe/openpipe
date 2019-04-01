"""
Produce metadata/content from a local or remote file
"""
import gzip
import bz2
import lzma
import mimetypes
from io import BytesIO
from os.path import splitext, expanduser
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_config = """
    path:                       # Local path or HTTP/HTTPS/FTP url
    """

    optional_config = """
    # The mime_type will be used by the action to identify and automatically
    # decode the file content.
    # With the default value of 'auto' the action will try to guess the
    # mime type based on the content header or file extension.
    mime_type:  auto

    # The following option is only applicable to local filenames
    auto_expand_home: True      # Expand '~' on path to user home dir
    """

    """
    This action can be extended with mime type decoders, on start it will load
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
        else:
            mime_type = mimetypes.guess_type(path)[0]

        forced_mime_type = self.config.get("mime_type")
        if forced_mime_type != "auto":
            mime_type = forced_mime_type

        if path == "-":
            return self.decode(BytesIO(item), mime_type)

        with open_func(path) as file:

            # mime type can be overridden from the action config
            if self.config["mime_type"] != "auto":
                mime_type = self.config["mime_type"]
            self.decode(file, mime_type)

    def decode(self, fileobj, mime_type, sender_action=None):
        if mime_type is None:
            mime_type = "text/plain"
        decoder_function = self.MIME_FILE_HANDLER.get(mime_type)
        if decoder_function:
            decoder_function(fileobj, sender_action or self)
        else:
            data = fileobj.read()
            self.put(data)
