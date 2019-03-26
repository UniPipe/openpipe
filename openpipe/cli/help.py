import os
import click
from os.path import exists
from sys import stderr
from mdvl import render
from importlib import import_module
from terminaltables import SingleTable
from ..utils import action2module, get_actions_metadata
from ..client.pretty import pretty_print_yaml


def config_markdown(config_string):
    config_string = config_string.lstrip("\r\n").rstrip(" ")
    markdown = ""
    for line in config_string.splitlines():
        markdown += line
        markdown += "\n"
    return markdown


def example_markdown(example_string):
    markdown = ""
    for line in example_string.splitlines():
        markdown += "    " + line + "\n"
    return markdown


@click.command(name="help")
@click.argument("plugin", nargs=-1, required=False)
def cmd_help(plugin):
    if len(plugin) == 0:
        return print_list_of_plugins()
    md_path = action2module(" ".join(plugin))
    try:
        plugin_module = import_module(md_path)
    except ModuleNotFoundError:
        print("No plugin with name: %s" % md_path, file=stderr)
        print("You can get a list of plugins with:")
        print("openpipe help")
        exit(2)

    examples_filename = plugin_module.__file__.rsplit(".", 1)[0] + "_examples.yaml"
    test_filename = plugin_module.__file__.rsplit(".", 1)[0]
    if test_filename[-1] != "_":
        test_filename += "_"
    test_filename += "test.yaml"
    plugin_purpose = plugin_module.__doc__
    triggers = ""
    if hasattr(plugin_module.Plugin, "on_input"):
        triggers += "- Input item is received\n"
    if hasattr(plugin_module.Plugin, "on_finish"):
        triggers += "- Input is closed\n"
    if hasattr(plugin_module.Plugin, "required_config"):
        config_string = plugin_module.Plugin.required_config
        config_string = config_markdown(config_string)
        required_config_md = "\n# Required Configuration\n" + config_string + "\n"
    else:
        required_config_md = ""
    if hasattr(plugin_module.Plugin, "optional_config"):
        config_string = plugin_module.Plugin.optional_config
        config_string = config_markdown(config_string)
        optional_config_md = "\n# Optional Configuration\n" + config_string + "\n"
    else:
        optional_config_md = ""

    cols, _ = os.get_terminal_size(0)
    if not exists(examples_filename) and exists(test_filename):
        examples_filename = test_filename

    if exists(examples_filename):
        example_md = "# Example(s)"
    else:
        example_md = ""

    markdown = """# Purpose\
    {}
{}{}{}
    """.format(
        plugin_purpose, required_config_md, optional_config_md, example_md
    )
    render(markdown, cols=cols)
    pretty_print_yaml(examples_filename)


def print_list_of_plugins():

    table_data = [["Action Name", "Purpose"]]
    for action_metadata in get_actions_metadata():
        table_data.append((action_metadata["name"], action_metadata["purpose"]))
    table = SingleTable(table_data)
    print(table.table)
    # print("-------------------------------------\n")
    print("You can get help for a plugin with:\nopenpipe help <plugin_name>")
