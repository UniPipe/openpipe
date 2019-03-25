"""
Produce file metadata and content from a TAR archive
"""
import tarfile

from ..file_ import Plugin


def decode_file(fileobj, plugin):

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


Plugin.attach_file_handler(decode_file, "application/x-tar")
