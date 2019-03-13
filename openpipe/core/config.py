from openpipe.core.yaml import load_yaml
from sys import stderr
from pprint import pformat


def check_missing(required_config, provided_config, required_config_str, plugin_label):
    """ Check if all required config was provided """
    for key, name in required_config.items():
        if key not in provided_config:
            print("Invalid configuration for", plugin_label, file=stderr)
            print("The mandatory field '%s' is missing" % key, plugin_label, file=stderr)
            print("The following configurations is required:", required_config_str, file=stderr)
            exit(3)


def validate_required_config(module_plugin, plugin_label, provided_config):
    """ """
    required_config_str = getattr(module_plugin, 'required_config', None)
    if not required_config_str:
        return None

    required_config = load_yaml(required_config_str)
    del required_config['__line__']

    # Required config must be a dict
    assert(isinstance(required_config, dict))

    # all the _dict_ values must be set to None
    for value in required_config.values():
        assert(value is None)

    config = {}
    required_config = load_yaml(required_config_str)

    if isinstance(provided_config, dict):
        for key in required_config:
            try:
                config[key] = provided_config[key]
            except KeyError:
                print("Invalid configuration for", plugin_label, file=stderr)
                print("The required field '%s' is missing" % key, plugin_label, file=stderr)
                print("The following configurations is required:", required_config_str, file=stderr)
                exit(3)
            del provided_config[key]
    else:
        if len(list(required_config.keys())) == 1:
            config[next(iter(required_config))] = provided_config
            provided_config = None
        else:
            print("Invalid configuration for", plugin_label, file=stderr)
            print("Got", type(provided_config), pformat(provided_config), file=stderr)
            print("Expected dictionary with fields", required_config_str, file=stderr)
            exit(4)
    return config


def validate_optional_config(required_config, module_plugin, plugin_label, provided_config):
    """ validate optional config and return the complete config """
    required_config_str = getattr(module_plugin, 'required_config', None)
    if not required_config_str:
        return None

    required_config = load_yaml(required_config_str)
    del required_config['__line__']


def validated_config(module_plugin, plugin_label, provided_config):
    """ Validate that the provided_config is valid per the plugin config schema """
    required_config = validate_required_config(module_plugin, plugin_label, provided_config)
    config = validate_optional_config(required_config, module_plugin, plugin_label, provided_config)

    return config
