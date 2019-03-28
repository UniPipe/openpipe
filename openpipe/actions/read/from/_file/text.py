"""
Produce content from a xml file
"""
from ..file_ import Plugin


def decode_file(fileobj, action):
    for line in fileobj:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.rstrip("\r\n")
        action.put(line)


Plugin.attach_file_handler(decode_file, "text/plain")
