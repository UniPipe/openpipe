"""
Produce dictionary items from JSON input items
"""
from pprint import pformat
from sys import stderr
from json import loads
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    content:        # Content to be parsed to json
    """

    def on_input(self, item):
        json_content = loads(self.config['content'])
        self.put(json_content)

    def sub_select(self, content, subset):    # NOQA: C901
        current_dict = dict()
        for key, value in subset.items():
            if isinstance(value, str):
                if value == ".":
                    value = key
                try:
                    source_item = content[key]
                except KeyError:
                    continue
                except TypeError:
                    print("E001 TypeError on XML parsing", file=stderr)
                    print("xml_dict (%s)" % type(content), file=stderr)
                    print("key=%s" % key, file=stderr)
                    print("xml_dict=%s" % pformat(content), file=stderr)
                    exit(1)
                current_dict[value] = source_item
            elif isinstance(value, dict):
                for subdict_key, subdict_value in value.items():
                    if subdict_key[0] == "@":
                        current_dict[subdict_value] = content[key][subdict_key]
                    else:
                        try:
                            sub_dict = content[key]
                        except KeyError:    # We simply ignore keys which are not found
                            continue
                        except TypeError:
                            print("E002 TypeError on XML parsing", file=stderr)
                            print("xml_dict (%s)" % type(content), file=stderr)
                            print("key=%s" % key, file=stderr)
                            print("xml_dict=%s" % pformat(content), file=stderr)
                        sub_result = self.extract_xml_dict(sub_dict, value)
                        current_dict.update(sub_result)
        return current_dict
