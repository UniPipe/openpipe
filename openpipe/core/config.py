from openpipe.core.yaml import load_yaml


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
