"""
Produce content from a xml file
"""
from ..file_ import Action


def decode_file(fileobj, action):
    for line in fileobj:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.rstrip("\r\n")
        action.put(line)


Action.attach_file_handler(decode_file, "text/plain")
Action.attach_file_handler(decode_file, "text/csv")
