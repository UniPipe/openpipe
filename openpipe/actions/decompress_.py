"""
Decompress gzip input item
"""
from openpipe.pipeline.engine import ActionRuntime
import zlib
import lzma
import bz2


class Action(ActionRuntime):

    category = "Data Transformation"

    optional_config = """
    path:   ""      # If not provided the input item is used
    type:   gzip    # the type to decompress
    """

    def on_input(self, item):
        ext_map = {
            "gzip": lambda x: zlib.decompress(x, 16 + zlib.MAX_WBITS),
            "xz": lambda x: lzma.decompress(x),
            "bzip": lambda x: bz2.decompress(x),
        }
        decompress_func = ext_map.get(self.config["type"])
        file_data = decompress_func(item)
        self.put(file_data)
