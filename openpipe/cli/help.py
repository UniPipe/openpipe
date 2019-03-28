import os
import click
from os.path import exists
from sys import stderr
from mdvl import render
from terminaltables import SingleTable
from ..utils import get_actions_metadata
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
@click.argument("action", nargs=-1, required=False)
def cmd_help(action):
    if len(action) == 0:
        return print_list_of_actions()
    action_name = " ".join(action)
    action = [
        action for action in get_actions_metadata() if action["name"] == action_name
    ]
    if not action:
        print("No action with name: %s" % action_name, file=stderr)
        print("You can get a list of actions with:")
        print("openpipe help")
        exit(2)

    action = action[0]
    test_filename = action["test_filename"]
    examples_filename = action.get("examples_filename", None) or test_filename

    config_string = action.get("required_config", None)
    if config_string is not None:
        config_string = config_markdown(config_string)
        required_config_md = "\n# Required Configuration\n" + config_string + "\n"
    else:
        required_config_md = ""
    config_string = action.get("optional_config", None)
    if config_string is not None:
        config_string = config_markdown(config_string)
        optional_config_md = "\n# Optional Configuration\n" + config_string + "\n"
    else:
        optional_config_md = ""

    cols, _ = os.get_terminal_size(0)
    if not exists(examples_filename) and exists(test_filename):
        examples_filename = test_filename

    #  if exists(examples_filename):
    #     example_md = "# Example(s)"
    #  else:
    #     example_md = ""
    example_md = ""

    markdown = """# Purpose\n\
    {}
{}{}{}
    """.format(
        action["purpose"], required_config_md, optional_config_md, example_md
    )
    render(markdown, cols=cols)
    pretty_print_yaml(examples_filename)


def print_list_of_actions():

    table_data = [["Action Name", "Purpose"]]
    for action_metadata in get_actions_metadata():
        table_data.append((action_metadata["name"], action_metadata["purpose"]))
    table = SingleTable(table_data)
    print(table.table)
    # print("-------------------------------------\n")
    print("You can get help for a action with:\nopenpipe help <action_name>")
