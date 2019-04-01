"""
This module provides action load and instantiation functions
"""
import traceback
import re
import sys
from sys import stderr
from os import getenv, getcwd
from os.path import splitext, join, dirname, expanduser, abspath
from importlib import import_module
from glob import glob
from wasabi import TracebackPrinter
from .action_config_schema import validate_config_schema
from .action_config import validate_provided_config


def action_module_name(action_name):
    """ returns the module name mapped from the action name """
    action_words = action_name.split(" ")
    package_name = action_words[:-1]
    module_name = action_words[-1] + "_"
    return "openpipe.actions." + (".".join(package_name + [module_name]))


def load_action_module(action_name, action_label):
    """ Load the python module associated with an action name """
    action_path = action_module_name(action_name)
    tb = TracebackPrinter(tb_base="openpipe", tb_exclude=("core.py",))
    try:
        action_module = import_module(action_path)
    except ModuleNotFoundError as error:
        print("Error loading module", action_path, file=stderr)
        print("Required for action:", action_label, file=stderr)
        error = tb("Module not found:", error.name, tb=traceback.extract_stack())
        raise ModuleNotFoundError(error) from None
    except ImportError as error:
        print("Error loading module", action_path, file=stderr)
        print("Required for action:", action_label, file=stderr)
        error = tb("ImportError", error.msg, tb=traceback.extract_stack())
        raise ImportError(error) from None
    if not hasattr(action_module, "Action"):
        print(
            "Module {} does not provide a Action class!".format(action_module),
            file=stderr,
        )
        print("Required for action:", action_label, file=stderr)
        raise NotImplementedError
    validate_config_schema(action_module.Action, action_label)
    return action_module


def yaml_attribute(text):
    text = text.strip("\n")
    text = text.rstrip("\n ")
    text = re.sub("^    ", "        ", text, flags=re.MULTILINE)
    return text


def create_action_instance(action_name, action_config, action_label):
    """ Create an instance for a module, after validating the provided config"""
    action_module = load_action_module(action_name, action_label)
    action_class = action_module.Action
    action_config = validate_provided_config(action_class, action_label, action_config)
    instance = action_class(action_config, action_label)
    return instance


def get_action_metadata(action_name, action_label):
    """ Get the metadata from an action module """
    action_module = load_action_module(action_name, action_label)
    action_class = action_module.Action

    filename, extension = splitext(action_module.__file__)
    filename = filename.strip("_")
    test_filename = filename + "_test.yaml"

    meta = {
        "name": action_name,
        "module_name": action_module_name(action_name).replace(".", "/") + ".py",
        "purpose": action_module.__doc__.splitlines()[1],
        "test_filename": test_filename,
    }

    for attribute_name in dir(action_class):
        if attribute_name[0] == "_":  # Skip internal attributes
            continue
        attribute_value = getattr(action_class, attribute_name)  # Skip non strings
        if not isinstance(attribute_value, str):
            continue
        meta[attribute_name] = yaml_attribute(attribute_value)
    return meta


def load_actions_paths():
    """
    Return a list of paths that should be used too search for action modules.
    The following order will be used:
    """
    action_search_list = []

    # ../actions/
    actions_dir = join(dirname(__file__), "..", "actions")
    action_search_list.append(actions_dir)

    # current directory/openpipe/actions
    cwd = getcwd()
    actions_dir = join(cwd, "openpipe", "actions")
    action_search_list.append(actions_dir)

    running_on_tox = getenv("TOX_ENV_NAME", False)
    if not running_on_tox:
        # ~/openpipe/libraries_cache/*/openpipe/actions
        search_pattern = join(
            expanduser("~"),
            ".openpipe",
            "libraries_cache",
            "*",
            "*",
            "openpipe",
            "actions",
        )
        for search_dir in glob(search_pattern):
            action_search_list.append(search_dir)

    # Add them to sys.path for action loading
    for action_path in action_search_list:
        base_lib_path = abspath(join(action_path, "..", ".."))
        sys.path.insert(0, base_lib_path)  # We will need to load the module

    action_search_list = [abspath(path) for path in action_search_list]

    return action_search_list


# We want action paths inserted on PYTHON path for any posterior loading
load_actions_paths()
