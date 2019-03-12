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


def validated_config(module_plugin, plugin_label, provided_config):  # NOQA: C901
    """ Validate that the provided_config matches the plugin supported config format """
    final_config = {}
    valid_keys = []
    required_config_str = getattr(module_plugin, 'required_config', None)
    optional_config_str = getattr(module_plugin, 'optional_config', None)

    required_config = load_yaml(required_config_str) if required_config_str else None
    optional_config = load_yaml(optional_config_str) if optional_config_str else None
    print("PROVCONFIG=", provided_config)
    print("RCONFIG=", required_config)
    print("OCONFIG=", optional_config)

    # Validate plugin configuration scheme
    if isinstance(required_config, dict):
        del required_config['__line__']
        for key, value in required_config.items():
            # Required config keys must not have a default value
            print("VAL=", value)
            assert(value is None)

    if isinstance(optional_config, dict):
        del optional_config['__line__']
        # Default config must provide values
        for key, value in optional_config.items():
            assert(value is not None)

    if required_config:
        valid_keys += required_config.keys()
        # a single key is required and a non dict was provided
        if not isinstance(provided_config, dict):
            required_config_keys = list(required_config.keys())
            if len(required_config_keys) == 1:
                print("GOT TMP")
                final_config[next(iter(required_config))] = provided_config
                provided_config = {}    # To be merged with default config, if any
            else:
                print("Invalid configuration format for", plugin_label, file=stderr)
                print("Got", type(provided_config), pformat(provided_config), file=stderr)
                print("Expected dictionary with fields", required_config_str, file=stderr)
                exit(3)
        else:
            check_missing(required_config, provided_config, required_config_str, plugin_label)

    if optional_config:
        if isinstance(optional_config, dict):
            valid_keys += optional_config.keys()
            if not isinstance(provided_config, dict):
                print("Invalid configuration format for", plugin_label, file=stderr)
                print("Got", type(provided_config), pformat(provided_config), file=stderr)
                print("Expected dictionary with fields", optional_config_str, file=stderr)
                exit(4)
            final_config = {**optional_config, **provided_config}
        else:
            final_config = provided_config

    if isinstance(provided_config, dict) and valid_keys:
        for key, value in provided_config.items():
            if key not in valid_keys:
                print("Invalid configuration key for", plugin_label, file=stderr)
                print("Unexpected key:\n", key, "=", value, file=stderr)
                print("Avaiable configuration keys", optional_config_str, file=stderr)
                exit(4)
    print("RESCONFIG=", final_config)
    if isinstance(final_config, dict) and isinstance(provided_config, dict):
        assert(len(final_config) >= len(provided_config))

    if not valid_keys and optional_config is None and provided_config is not None:
        print("Invalid configuration key for", plugin_label, file=stderr)
        print("Unexpected configuration:\n", provided_config, file=stderr)
        print("The plugin does not accept any configuration", file=stderr)

    return final_config
