from .yaml_extra import load_yaml


def validate_config_dict(action_plugin, config_group_name, value_check_func):

    try:
        config_group_str = getattr(action_plugin, config_group_name)
    except AttributeError:
        # Config items are all optional
        return

    config = load_yaml(config_group_str, False)

    if isinstance(config, dict):
        for key, value in config.items():
            assert " " not in key  # Spaces are not allowed in key names
            assert value_check_func(value)


def validate_config_schema(action_plugin, action_label):
    def mut_be_none(x):
        return x is None

    def mut_not_be_none(x):
        return x is not None

    validate_config_dict(action_plugin, "required_config", mut_be_none)
    validate_config_dict(action_plugin, "optional_config", mut_not_be_none)
