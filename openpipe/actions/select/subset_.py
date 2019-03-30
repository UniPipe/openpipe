"""
Select a subset of data from a dictionary input
"""
from pprint import pformat
from sys import stderr

from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Selection"

    required_some_config = """
    # YAML describing the elements to be retrieved
    """

    def on_input(self, item):
        new_item = self.sub_select(item, self.config)
        self.put(new_item)

    def sub_select(self, content, subset):
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
                        except KeyError:  # We simply ignore keys which are not found
                            continue
                        except TypeError:
                            print("E002 TypeError on XML parsing", file=stderr)
                            print("xml_dict (%s)" % type(content), file=stderr)
                            print("key=%s" % key, file=stderr)
                            print("xml_dict=%s" % pformat(content[:256]), file=stderr)
                            raise
                        sub_result = self.sub_select(sub_dict, value)
                        current_dict.update(sub_result)
        return current_dict
