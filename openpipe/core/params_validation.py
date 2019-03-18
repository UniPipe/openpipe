from openpipe.core.yaml import load_yaml
from sys import stderr
from pprint import pformat


def delete_line_info(some_dict):
    del some_dict['__line__']
    for value in some_dict.values():
        if isinstance(value, dict):
            delete_line_info(value)


def validate_requiredl_params(module_plugin, plugin_label, provided_params):
    """ """
    requiredl_params_str = getattr(module_plugin, 'requiredl_params', None)
    if requiredl_params_str is None:
        return {}

    requiredl_params = load_yaml(requiredl_params_str)

    # Required params must be a dict
    assert(isinstance(requiredl_params, dict))
    delete_line_info(requiredl_params)

    # all the _dict_ values must be set to None
    for key, value in requiredl_params.items():
        assert(' ' not in key)  # Spaces are not allowed in required key names
        assert(value is None)
    params = {}
    if isinstance(provided_params, dict):
        for key in requiredl_params:
            try:
                params[key] = provided_params[key]
            except KeyError:
                print("Invalid parameters for", plugin_label, file=stderr)
                print("The required field '%s' is missing" % key, plugin_label, file=stderr)
                print("The following parameters are required:", requiredl_params_str, file=stderr)
                exit(22)
            del provided_params[key]
    else:
        if len(list(requiredl_params.keys())) == 1:
            if provided_params is None:
                print("Invalid parameters for", plugin_label, file=stderr)
                print("The required field '%s' is missing" % key, plugin_label, file=stderr)
                print("The following parameters are required:", requiredl_params_str, file=stderr)
                exit(22)
            params[next(iter(requiredl_params))] = provided_params
        else:
            print("Invalid parameters for", plugin_label, file=stderr)
            print("Got", type(provided_params), pformat(provided_params), file=stderr)
            print("Expected dictionary with fields", requiredl_params_str, file=stderr)
            exit(21)
    return params


def validate_optional_params(requiredl_params, module_plugin, plugin_label, provided_params):
    """ validate optional params and return the complete params """
    optional_params_str = getattr(module_plugin, 'optional_params', None)
    if optional_params_str is not None:
        optional_params = load_yaml(optional_params_str)
        if isinstance(optional_params, dict):
            delete_line_info(optional_params)

            for key, value in optional_params.items():
                assert(' ' not in key)  # Spaces are not allowed in required key names
                # Optional params values can not be None
                assert(value is not None)

            merged_params = {**requiredl_params, **optional_params}
            if provided_params is None:
                return merged_params

            if requiredl_params and len(list(requiredl_params.keys())) == 1 \
                    and not isinstance(provided_params, dict):
                return merged_params

            if not isinstance(provided_params, dict):
                print("Invalid parameters for", plugin_label, file=stderr)
                print("Got", type(provided_params), pformat(provided_params), file=stderr)
                print("Expected dictionary with fields", optional_params_str, file=stderr)
                exit(23)

            for key in provided_params:
                if key not in optional_params:
                    print("The provide field '%s' is not supported" % key, plugin_label, file=stderr)
                    print("Expected dictionary with fields", optional_params_str, file=stderr)
                    exit(24)
            final_params = {**merged_params, **provided_params}
            return final_params
        else:
            # optional params can only be a non dict if required params is void
            assert(len(requiredl_params) == 0)
            return provided_params or optional_params
        return optional_params
    else:
        if provided_params:
            print("Unexpected params for", plugin_label, file=stderr)
            print("Got", type(provided_params), pformat(provided_params), file=stderr)
            print("The plugin does not support any kind of configuration", file=stderr)
            exit(20)
        return requiredl_params


def validate_params(module_plugin, plugin_label, provided_params):
    """ Validate that the provided_params is valid per the plugin params schema """

    if hasattr(module_plugin, "required_some_params"):
        if provided_params is None:
            print("Missing params for", plugin_label, file=stderr)
            print("The plugin requires parameters", file=stderr)
            exit(25)
        else:
            return provided_params

    requiredl_params = validate_requiredl_params(module_plugin, plugin_label, provided_params)
    # A single required item is required, a single item was provided, no optional params
    if len(requiredl_params) == 1 and not isinstance(provided_params, dict) \
            and not hasattr(module_plugin, 'optional_params'):
        return requiredl_params

    params = validate_optional_params(requiredl_params, module_plugin, plugin_label, provided_params)
    return params
