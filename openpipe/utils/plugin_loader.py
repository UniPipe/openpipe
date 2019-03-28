"""
This module provides the plugin_load function which performs the following:
    - map action names to python module files
    - import the plugin
    - create an instance of the Plugin class
    - validate the Plugin's config schema
    - validate that the user provided config meets the config schema requirements
"""
import traceback
import re
from sys import stderr
from importlib import import_module
from wasabi import TracebackPrinter
from .plugin_config_schema import validate_config_schema
from .plugin_config import validate_provided_config


def yaml_attribute(plugin_class, attribute_name):
    attribute_text = getattr(plugin_class, attribute_name, None)
    if attribute_text:
        attribute_text = attribute_text.strip("\n")
        attribute_text = attribute_text.rstrip("\n ")
        attribute_text = re.sub("^    ", "        ", attribute_text, flags=re.MULTILINE)
    return attribute_text


def get_action_metadata(action_name, action_label):
    action_module = load_action_module(action_name, action_name)
    plugin_class = action_module.Plugin
    meta = {
        "purpose": action_module.__doc__,
        "required_config": yaml_attribute(plugin_class, "required_config"),
        "optional_config": yaml_attribute(plugin_class, "optional_config"),
        "required_some_config": yaml_attribute(plugin_class, "required_some_config"),
    }
    return meta


def create_action_instance(action_name, action_config, action_label, meta_only=False):
    action_module = load_action_module(action_name, action_name)
    plugin_class = action_module.Plugin
    action_config = validate_provided_config(plugin_class, action_label, action_config)
    instance = plugin_class(action_config, action_label)
    return instance


def load_action_module(action_name, action_label):
    """ Load the python module associated with an action name """
    plugin_path = action2module(action_name)
    try:
        action_module = import_module(plugin_path)
    except ModuleNotFoundError as error:
        print("Error loading module", plugin_path, file=stderr)
        tb = TracebackPrinter(tb_base="openpipe", tb_exclude=("core.py",))
        error = tb("Module not found:", error.name, tb=traceback.extract_stack())
        raise ModuleNotFoundError(error) from None
    except ImportError as error:
        print("Error loading module", plugin_path, file=stderr)
        error = tb("ImportError", error.name, tb=traceback.extract_stack())
        print("Required for action:", action_label, file=stderr)
        raise ImportError(error) from None
    if not hasattr(action_module, "Plugin"):
        print("Module {} does not provide a Plugin class!".format(action_module), file=stderr)
        print("Required for action:", action_label, file=stderr)
        raise NotImplementedError
    validate_config_schema(action_module.Plugin, action_label)
    return action_module


def action2module(action_name):
    action_words = action_name.split(" ")
    package_name = action_words[:-1]
    module_name = action_words[-1] + "_"
    return "openpipe.plugins." + (".".join(package_name + [module_name]))
