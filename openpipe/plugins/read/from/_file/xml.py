"""
Produce content from a xml file
"""
from ..file import Plugin
import xmltodict


def decode_file(fileobj, plugin):
    data = fileobj.read()
    xml_data = xmltodict.parse(data)
    plugin.put(xml_data)


Plugin.attach_file_handler(decode_file, "application/xml")
Plugin.attach_file_handler(decode_file, "text/xml", decode_file)
