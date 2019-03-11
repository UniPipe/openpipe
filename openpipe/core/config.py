from openpipe.core.yaml import load_yaml
from sys import stderr
from pprint import pformat


def parse_default_config(config_string):
    """ Build a config string dict from a default config string """
    config = load_yaml(config_string)
    if isinstance(config, dict):
        config_dict = {}
        # Remove the "*" default field from field name
        for key, value in config.items():
            key = key.strip('*')
            config_dict[key] = value
        return config_dict

    else:
        return config


def validated_config(provided_config, default_config, plugin_label):
    """ Validate that the provided_config matches the default config format """
    #  print(plugin_label, provided_config, default_config, )
    parsed_default_config = parse_default_config(default_config)
    if isinstance(parsed_default_config, dict):
        if not isinstance(provided_config, dict):
            print("Invalid configuration format for", plugin_label, file=stderr)
            print("Got", type(provided_config), pformat(provided_config), file=stderr)
            print("Expected dictionary with fields", default_config, file=stderr)
            exit(4)
        for key, value in provided_config.items():
            if key not in default_config:
                print("Invalid configuration key for", plugin_label, file=stderr)
                print("Unexpected key:\n", key, "=", value, file=stderr)
                print("Avaiable configuration keys", default_config, file=stderr)
                exit(4)
        return {**parsed_default_config, **provided_config}
    return parsed_default_config
