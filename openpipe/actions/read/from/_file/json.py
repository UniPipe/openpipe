"""
Produce content from a json file
"""
from json import load
from ..file_ import Plugin


def decode_file(fileobj, action):
    json_data = load(fileobj)
    action.put(json_data)


Plugin.attach_file_handler(decode_file, "application/json")
