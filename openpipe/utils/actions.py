""" This module provides functions to get metadata from actions """
import os
from os.path import splitext
from .action_loader import get_action_metadata, load_actions_paths


def get_actions_metadata():
    """ Extract metadata from modules """
    action_list = []

    for action_path in load_actions_paths():
        for root, dirs, files in os.walk(action_path, topdown=True):
            # Skip submodules
            if root.split(os.sep)[-1][0] == "_":
                continue
            action_root = root.split(os.sep)[len(action_path.split(os.sep)) :]
            for filename in files:
                filename, extension = splitext(filename)
                if not extension == ".py":
                    continue
                action_name = filename.strip("_")
                if action_root:
                    action_name = " ".join(action_root) + " " + action_name
                find_action = [
                    action for action in action_list if action["name"] == action_name
                ]
                if find_action:
                    continue
                try:
                    action_metadata = get_action_metadata(
                        action_name, "get_actions_metadata()"
                    )
                except:  # NOQA: E722
                    # Ignore broken modules
                    continue
                action_list.append(action_metadata)
    action_list.sort(key=lambda x: x["name"])
    return action_list
