import os
from os.path import join
from re import findall


class ActionInfo:
    def __init__(self, name, purpose, test):
        self.name = name
        self.purpose = purpose
        self.test = test


def get_actions():
    action_list = []
    import openpipe.plugins

    for path in openpipe.plugins.__path__:
        for root, dirs, files in os.walk(path, topdown=True):
            if root.endswith("__pycache__"):
                continue
            # Skip submodules
            if root.split(os.sep)[-1][0] == "_":
                continue
            plugin_path = root[len(path) :].strip(os.sep).replace(os.sep, " ")
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
    return action_list
