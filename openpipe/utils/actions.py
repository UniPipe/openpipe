""" This module provides functions to get metadata from  actions """
import os
import sys
from os.path import join, dirname, abspath
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
    plugins_dir = join(cwd, "openpipe", "plugins")
    action_search_list.append(plugins_dir)

    running_on_tox = os.getenv("TOX_ENV_NAME", False)
    if not running_on_tox:
        # ~/openpipe/libraries_cache/*/openpipe/plugins
        search_pattern = join(
            expanduser("~"),
            ".openpipe",
            "libraries_cache",
            "*",
            "*",
            "openpipe",
            "plugins",
        )
        for search_dir in glob(search_pattern):
            action_search_list.append(search_dir)

    action_search_list = [abspath(path) for path in action_search_list]
    return action_search_list


def get_actions_metadata():
    """ Extract metadata from modules """
    action_list = []

    for action_path in get_actions_paths():
        base_lib_path = abspath(join(action_path, "..", ".."))
        sys.path.insert(0, base_lib_path)  # We will need to load the module
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
                examples_filename = join(
                    root, filename.replace(".py", "").strip("_") + "_examples.yaml"
                )
                action_name = plugin_path + " " if plugin_path else ""
                action_name += " ".join((plugin_name).split(" ")).strip("_")
                find_action = [
                    action for action in action_list if action["name"] == action_name
                ]
                if find_action:
                    continue
                metadata = plugin_load(action_name, None, None, meta_only=True)
                purpose = metadata["purpose"].splitlines()[1]
                action = {
                    "name": action_name,
                    "purpose": purpose,
                    "required_config": metadata["required_config"],
                    "optional_config": metadata["optional_config"],
                }
                if exists(examples_filename):
                    action["examples_file_name"] = examples_filename
                    with open(examples_filename) as examples_filename:
                        action["examples_file_content"] = examples_filename.read()

                if exists(test_filename):
                    action["test_file_name"] = test_filename
                    with open(test_filename) as test_file:
                        action["test_file_content"] = test_file.read()
                else:
                    raise Exception("Action mustprovide a test file")
                # If no examples are available, failback to tests
                if not action.get("examples_file_name", None):
                    action["examples_file_name"] = test_filename
                    action["examples_file_content"] = action["test_file_content"]

                action_list.append(action)
    action_list.sort(key=lambda x: x["name"])
    return action_list
