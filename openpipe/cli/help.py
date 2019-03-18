import os
import re
import click
from sys import stderr
from os.path import join, exists
from mdvl import render
from importlib import import_module
from terminaltables import SingleTable
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import YamlLexer


def config_markdown(config_string):
    config_string = config_string.lstrip('\r\n').rstrip(' ')
    markdown = ''
    for line in config_string.splitlines():
        markdown += line
        markdown += '\n'
    return markdown


def example_markdown(example_string):
    markdown = ''
    for line in example_string.splitlines():
        markdown += "    "+line+"\n"
    return markdown


@click.command()
@click.argument('plugin', nargs=-1, required=False)
def help(plugin):
    if len(plugin) == 0:
        return print_list_of_plugins()
    md_path = "openpipe.plugins."
    md_path += '.'.join(plugin)
    for plugin_part in plugin:
        md_path + "." + plugin_part
    try:
        plugin_module = import_module(md_path)
    except ModuleNotFoundError:
        print("No plugin with name: %s" % md_path, file=stderr)
        print("You can get a list of plugins with:")
        print("openpipe help")
        exit(2)

    examples_filename = plugin_module.__file__.rsplit('.', 1)[0] + "_examples.yaml"
    plugin_purpose = plugin_module.__doc__
    triggers = ''
    if hasattr(plugin_module.Plugin, 'on_input'):
        triggers += "- Input item is received\n"
    if hasattr(plugin_module.Plugin, 'on_finish'):
        triggers += "- Input is closed\n"
    if hasattr(plugin_module.Plugin, 'required_params'):
        config_string = plugin_module.Plugin.required_params
        config_string = config_markdown(config_string)
        required_params_md = "\n# Required Parameters\n" + config_string + "\n"
    else:
        required_params_md = ''
    if hasattr(plugin_module.Plugin, 'optional_params'):
        config_string = plugin_module.Plugin.optional_params
        config_string = config_markdown(config_string)
        optional_params_md = "\n# Optional Parameters\n" + config_string + "\n"
    else:
        optional_params_md = ''

    cols, _ = os.get_terminal_size(0)

    if exists(examples_filename):
        example_md = "# Example(s)"
    else:
        example_md = ''

    markdown = """# Purpose\
    {}
{}{}{}
    """.format(plugin_purpose, required_params_md, optional_params_md, example_md)

    render(markdown, cols=cols)

    if exists(examples_filename):
        with open(examples_filename) as yaml_content:
            print(highlight(yaml_content.read(), YamlLexer(), TerminalTrueColorFormatter()))


def print_list_of_plugins():
    available_plugins = {}  # When running from source, the same module with be found in multiple paths
    import openpipe.plugins
    for path in openpipe.plugins.__path__:
        for root, dirs, files in os.walk(path, topdown=True):
            if root.endswith('__pycache__'):
                continue
            plugin_path = root[len(path):].strip(os.sep).replace(os.sep, ' ')
            for filename in files:
                if not filename.endswith('.py'):
                    continue
                plugin_filename = join(root, filename)
                plugin_name = filename.replace('.py', '')
                plugin_fullname = ''
                if plugin_path:
                    plugin_fullname += plugin_path+" "
                plugin_fullname += plugin_name
                if plugin_fullname in available_plugins:
                    continue
                available_plugins[plugin_fullname] = plugin_filename

    table_data = [["Action", "Description"]]
    for name in sorted(available_plugins.keys()):
        filename = available_plugins[name]
        with open(filename) as module_file:
            filedata = module_file.read()
            purpose = re.findall('"""\n([^\n]*)', filedata)
            if not purpose or '#' in purpose[0]:
                print("Error on", filename)
                exit(1)
            purpose = purpose[0] if purpose else ''
            # actions descriptions with a leading _ means it should be hidden
            # from the actions list (for internal actions)
            if purpose and purpose[0] == '_':
                continue
            table_data.append([name, purpose])
    table = SingleTable(table_data)
    print(table.table)
    # print("-------------------------------------\n")
    # print("You can get help for a plugin with:\nopenpipe help <plugin_name>")
