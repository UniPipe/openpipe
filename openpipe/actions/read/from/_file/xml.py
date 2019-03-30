"""
Produce content from a xml file
"""
from ..file_ import Action
import xmltodict


def decode_file(fileobj, action):
    data = fileobj.read()
    xml_data = xmltodict.parse(data)
    action.put(xml_data)


Action.attach_file_handler(decode_file, "application/xml")
Action.attach_file_handler(decode_file, "text/xml")
