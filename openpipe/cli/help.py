import os
import re
import click
from sys import stderr
from os.path import join
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
    markdown = plugin_module.__doc__.replace("```yaml", "```")
    render(markdown, cols=80)


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
            purpose = re.findall('## Purpose[\r\n]+([^\r\n]+)', filedata)
            if len(purpose) == 1:
                purpose = '# '+purpose[0]
            else:
                purpose = ''
        print(name, purpose)

    print("-------------------------------------\n")
    print("You can get help for a plugin with:\nopenpipe help <plugin_name>")
