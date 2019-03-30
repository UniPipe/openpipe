"""
Produce content from a xml file
"""
from ..file_ import Plugin
import xmltodict


def decode_file(fileobj, action):
    data = fileobj.read()
    xml_data = xmltodict.parse(data)
    action.put(xml_data)


Plugin.attach_file_handler(decode_file, "application/xml")
Plugin.attach_file_handler(decode_file, "text/xml")
