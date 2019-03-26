from yaml import Loader, load
from yaml.composer import Composer
from yaml.parser import ParserError
from yaml.constructor import Constructor


# Ignore deprecation warnings, until we have a PYAML release containing the PR:
#  https://github.com/yaml/pyyaml/pull/212
#
# https://stackoverflow.com/a/50519680/401041
def warn(*args, **kwargs):
    pass


import warnings  # NOQA: E402

warnings.warn = warn


def load_yaml(data, include_line_number=True):
    """
    Load YAML data extending it with line number information, nodes get a __line__ attribute
    """
    if not include_line_number:
        return load(data)

    loader = Loader(data)

    def compose_node(parent, index):
        # the line number where the previous token has ended (plus empty lines)
        line = loader.line
        node = Composer.compose_node(loader, parent, index)
        node.__line__ = line + 1
        return node

    def construct_mapping(node, deep=False):
        mapping = Constructor.construct_mapping(loader, node, deep=deep)
        mapping["__line__"] = node.__line__
        return mapping

    loader.compose_node = compose_node
    loader.construct_mapping = construct_mapping
    # The YAML ParserError traceback info is not very usefull
    try:
        data = loader.get_single_data()
    except ParserError as error:
        print("Syntax error parsing the YAML")
        print(error)
        exit(1)
    return data


def remove_line_info(yaml_dict):
    if yaml_dict and isinstance(yaml_dict, dict):
        try:
            del yaml_dict["__line__"]
        except KeyError:
            pass
        for key, value in yaml_dict.items():
            remove_line_info(value)
    if yaml_dict and isinstance(yaml_dict, list):
        for value in yaml_dict:
            remove_line_info(value)
