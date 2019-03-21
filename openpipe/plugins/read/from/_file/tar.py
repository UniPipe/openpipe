"""
Produce file metadata and content from a TAR archive
"""
#  from blinker import signal
import tarfile

from ..file import attach_file_handler


def read_from_tar_file(self, fileobj, file_extension, mime_type, plugin):

    #  print("Checking", file_extension, mime_type)

    with tarfile.open(fileobj=fileobj) as tar:
        while True:
            file_info = tar.next()
            if file_info is None:  # Reached end of archive
                break
            if not file_info.isfile():
                continue
            single_file = tar.extractfile(file_info)
            new_item = {}
            new_item["name"] = file_info.name
            new_item["content"] = single_file.read()
            single_file.close()
            plugin.put(new_item)

    return True


attach_file_handler(read_from_tar_file, ".tar", "application/x-tar")

#  read_from_file = signal("read from file")
#  read_from_file.connect(read_from_tar_file)
