"""
Produce file properties and content from a TAR archive
"""

from openpipe.engine import PluginRuntime
import tarfile
from io import BytesIO


class Plugin(PluginRuntime):

    optional_config = """
    $_$     # The path to to the tar file, "-" to use the input item
    """

    def on_input(self, item):
        name = self.config
        if name == '-':
            name = None
            fileobj = BytesIO(item)
        else:
            fileobj = None
        with tarfile.open(name=name, fileobj=fileobj) as tar:
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
