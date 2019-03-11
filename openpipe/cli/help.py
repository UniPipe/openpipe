import os
import re
import click
from sys import stderr
from os.path import join, abspath
from mdvl import render
from importlib import import_module


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
    plugin_purpose = plugin_module.__doc__
    triggers = ''
    if hasattr(plugin_module.Plugin, 'on_input'):
        triggers += "- Input item is received\n"
    if hasattr(plugin_module.Plugin, 'on_complete'):
        triggers += "- Input is closed\n"
    if hasattr(plugin_module.Plugin, 'default_config'):
        config_string = plugin_module.Plugin.default_config
        default_config_md = "# Configuration\n" + config_string.rstrip(' \t\r\n')
    else:
        default_config_md = ''
    test_file = abspath(join(__file__, '..', '..', 'tests', 'plugins', os.sep.join(plugin)))+".yaml"

    cols, _ = os.get_terminal_size(0)

    markdown = """# Purpose\
    {}
# Trigger(s)
{}
{}

# Example(s)
{}
    """.format(plugin_purpose, triggers, default_config_md, test_file)
    render(markdown, cols=cols)


def print_list_of_plugins():
    available_plugins = {}  # When running from source, the same module with be found in multiple paths
    print("---- List of available plugins ----")
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

    for name in sorted(available_plugins.keys()):
        filename = available_plugins[name]
        with open(filename) as module_file:
            filedata = module_file.read()
            purpose = re.findall('"""\n([^\n]*)', filedata)
            if not purpose or '#' in purpose[0]:
                print("Error on", filename)
                exit(1)
            purpose = '# '+purpose[0] if purpose else ''
        print('{:30}  {:>12}'.format(name, purpose))

    print("-------------------------------------\n")
    print("You can get help for a plugin with:\nopenpipe help <plugin_name>")
