""" This module provides functions to get metadata from  actions """
import os
from os.path import join, dirname
from os.path import expanduser, exists
from glob import glob
from .plugin_loader import plugin_load


def get_actions_paths():
    """
    Return a list of paths that should be used too search for action modules.
    The following order will be used:
    """
    action_search_list = []

    # ../plugins/
    plugins_dir = join(dirname(__file__), "..", "plugins")
    action_search_list.append(plugins_dir)

    # current directory/openpipe/plugins
    cwd = os.getcwd()
    plugins_dir = join(cwd, "..", "plugins")
    action_search_list.append(plugins_dir)

    # ~/openpipe/libraries_cache/*/openpipe/plugins
    search_pattern = join(
        expanduser("~"), ".openpipe", "libraries_cache", "*", "*", "openpipe", "plugins"
    )
    for search_dir in glob(search_pattern):
        action_search_list.append(search_dir)

    return action_search_list


def get_actions_metadata():
    """ Extract metadata from modules """
    action_list = []

    for action_path in get_actions_paths():
        for root, dirs, files in os.walk(action_path, topdown=True):
            # Skip submodules
            if root.split(os.sep)[-1][0] == "_":
                continue
            plugin_path = root[len(action_path) :].strip(os.sep).replace(os.sep, " ")
            for filename in files:
                if not filename.endswith(".py"):
                    continue
                plugin_name = filename.replace(".py", "")
                test_filename = join(
                    root, filename.replace(".py", "").strip("_") + "_test.yaml"
                )
                plugin_fullname = ""
                if plugin_path:
                    plugin_fullname += plugin_path + " "
                plugin_fullname += plugin_name
                [action for action in action_list if action["name"] == plugin_fullname]
                if plugin_fullname in action_list:
                    continue
                plugin_fullname = plugin_fullname.replace("_", " ")
                plugin_fullname = plugin_fullname.strip(" ")
                metadata = plugin_load(plugin_fullname, None, None, meta_only=True)
                purpose = metadata["purpose"].splitlines()[1]
                action = {
                    "name": plugin_fullname,
                    "purpose": purpose,
                    "required_config": metadata["required_config"],
                    "optional_config": metadata["optional_config"],
                }
                if exists(test_filename):
                    action["test_file_name"] = test_filename
                    with open(test_filename) as test_file:
                        action["test_file_content"] = test_file.read()
                action_list.append(action)
    action_list.sort(key=lambda x: x["name"])
    return action_list
