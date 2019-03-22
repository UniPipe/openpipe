"""
Produce content from a xml file
"""
from ..file import Plugin


def decode_file(fileobj, plugin):
    for line in fileobj:
        line = line.decode("utf-8")
        line = line.rstrip("\r\n")
        plugin.put(line)


Plugin.attach_file_handler(decode_file, "text/plain")
