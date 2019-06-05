"""
Produce file metadata and content from a TAR archive
"""
import tarfile

from ..file_ import Action


def decode_file(fileobj, action):

    selected_file = action.config.get("select", "")
    with tarfile.open(fileobj=fileobj) as tar:
        while True:
            file_info = tar.next()
            if file_info is None:  # Reached end of archive
                break
            if not file_info.isfile():
                continue
            if selected_file and selected_file != file_info.name:
                continue
            single_file = tar.extractfile(file_info)
            new_item = {}
            new_item["filename"] = file_info.name
            new_item["content"] = single_file.read()
            action.put(new_item)
            single_file.close()
            if selected_file:  # Found the file was searching for
                break
    return True


Action.attach_file_handler(decode_file, "application/x-tar")
