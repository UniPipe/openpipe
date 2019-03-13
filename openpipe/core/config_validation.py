from openpipe.core.yaml import load_yaml
from sys import stderr
from pprint import pformat


def validate_required_config(module_plugin, plugin_label, provided_config):
    """ """
    required_config_str = getattr(module_plugin, 'required_config', None)
    if required_config_str is None:
        return {}

    required_config = load_yaml(required_config_str)

    # Required config must be a dict
    assert(isinstance(required_config, dict))
    del required_config['__line__']

    # all the _dict_ values must be set to None
    for key, value in required_config.items():
        assert(' ' not in key)  # Spaces are not allowed in required key names
        assert(value is None)
    config = {}
    if isinstance(provided_config, dict):
        for key in required_config:
            try:
                config[key] = provided_config[key]
            except KeyError:
                print("Invalid configuration for", plugin_label, file=stderr)
                print("The required field '%s' is missing" % key, plugin_label, file=stderr)
                print("The following configuration is required:", required_config_str, file=stderr)
                exit(22)
            del provided_config[key]
    else:
        if len(list(required_config.keys())) == 1:
            config[next(iter(required_config))] = provided_config
        else:
            print("Invalid configuration for", plugin_label, file=stderr)
            print("Got", type(provided_config), pformat(provided_config), file=stderr)
            print("Expected dictionary with fields", required_config_str, file=stderr)
            exit(21)
    return config


def validate_optional_config(required_config, module_plugin, plugin_label, provided_config):
    """ validate optional config and return the complete config """
    optional_config_str = getattr(module_plugin, 'optional_config', None)
    if optional_config_str is not None:
        optional_config = load_yaml(optional_config_str)
        if isinstance(optional_config, dict):
            del optional_config['__line__']

            for key, value in optional_config.items():
                assert(' ' not in key)  # Spaces are not allowed in required key names
                # Optional config values can not be None
                assert(value is not None)

            merged_config = {**required_config, **optional_config}
            if provided_config is None:
                return merged_config

            if not isinstance(provided_config, dict):
                print("Invalid configuration for", plugin_label, file=stderr)
                print("Got", type(provided_config), pformat(provided_config), file=stderr)
                print("Expected dictionary with fields", optional_config_str, file=stderr)
                exit(23)

            for key in provided_config:
                if key not in optional_config:
                    print("The provide field '%s' is not supported" % key, plugin_label, file=stderr)
                    print("Expected dictionary with fields", optional_config_str, file=stderr)
                    exit(24)
            final_config = {**merged_config, **provided_config}
            return final_config
        else:
            # optional config can only be a non dict if required config is void
            assert(len(required_config) == 0)
            return provided_config or optional_config
        return optional_config
    else:
        if provided_config:
            print("Unexpected config for", plugin_label, file=stderr)
            print("Got", type(provided_config), pformat(provided_config), file=stderr)
            print("The plugin doet not support any kind of configuration", file=stderr)
            exit(20)
        return required_config


def validate_config(module_plugin, plugin_label, provided_config):
    """ Validate that the provided_config is valid per the plugin config schema """

    if hasattr(module_plugin, "required_some_config"):
        if provided_config is None:
            print("Missing config for", plugin_label, file=stderr)
            print("The plugin requires configuration parameters", file=stderr)
            exit(25)
        else:
            return provided_config

    required_config = validate_required_config(module_plugin, plugin_label, provided_config)
    # A single required item is required, a single item was provided, no optional config
    if len(required_config) == 1 and not isinstance(provided_config, dict) \
            and not hasattr(module_plugin, 'optional_config'):
        return required_config

    config = validate_optional_config(required_config, module_plugin, plugin_label, provided_config)
    return config
