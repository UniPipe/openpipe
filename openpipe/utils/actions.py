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
                action_metadata = get_action_metadata(
                    action_name, "get_actions_metadata()"
                )
                """
                if exists(examples_filename):
                    action_metadata["examples_file_name"] = examples_filename
                    with open(examples_filename) as examples_filename:
                        action_metadata[
                            "examples_file_content"
                        ] = examples_filename.read()

                if exists(test_filename):
                    action_metadata["test_file_name"] = test_filename
                    with open(test_filename) as test_file:
                        action_metadata["test_file_content"] = test_file.read()
                else:
                    raise Exception("Action mustprovide a test file")
                # If no examples are available, failback to tests
                if not action_metadata.get("examples_file_name", None):
                    action_metadata["examples_file_name"] = test_filename
                    action_metadata["examples_file_content"] = action_metadata[
                        "test_file_content"
                    ]
                """
                action_list.append(action_metadata)
    action_list.sort(key=lambda x: x["name"])
    return action_list
