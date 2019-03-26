""" This module provides functions to get metadata from  actions """
import os
from os.path import join, dirname
from re import findall
from os.path import expanduser
from glob import glob


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
    #  libraries_cache_dir = join(expanduser("~"), ".openpipe", "libraries_cache")
    #  for libdirname in glob(join(libraries_cache_dir, '*'))


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
                plugin_filename = join(root, filename)
                plugin_name = filename.replace(".py", "")
                plugin_fullname = ""
                if plugin_path:
                    plugin_fullname += plugin_path + " "
                plugin_fullname += plugin_name
                [action for action in action_list if action["name"] == plugin_fullname]
                if plugin_fullname in action_list:
                    continue
                plugin_fullname = plugin_fullname.replace("_", " ")
                plugin_fullname = plugin_fullname.strip(" ")
                with open(plugin_filename) as module_file:
                    filedata = module_file.read()
                    purpose = findall('"""\n([^\n]*)', filedata)
                    if not purpose or "#" in purpose[0]:
                        print("Purpose docstring error on", plugin_filename)
                        exit(1)
                    purpose = purpose[0] if purpose else ""
                action = {"name": plugin_fullname, "purpose": purpose}
                action_list.append(action)
    action_list.sort(key=lambda x: x["name"])
    return action_list
