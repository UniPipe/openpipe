"""
Produce content from a json file
"""
from json import load
from ..file import Plugin


def decode_file(fileobj, plugin):
    json_data = load(fileobj)
    plugin.put(json_data)


Plugin.attach_file_handler(decode_file, "application/json")
