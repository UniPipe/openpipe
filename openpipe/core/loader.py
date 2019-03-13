"""
This file provides a PluginLoader class which is responsible for importing
a plugin's module and instantiate it's class
"""
from sys import stderr
from importlib import import_module
from traceback import format_exc
from os.path import join, normpath
from .config_validation import validate_config


class CoreLoader(object):

    def load(self, plugin_filename, pipeline_filename, name, config, line_nr):
        if pipeline_filename[0] not in ['.', '/']:
            pipeline_filename = join('.', pipeline_filename)
        plugin_label = "'{}', file \"{}\", line {}".format(name, pipeline_filename, line_nr)
        try:
            module = import_module(plugin_filename)
        except ModuleNotFoundError:
            print(format_exc(), file=stderr)
            print('Required for step:', plugin_label, file=stderr)
            exit(1)
        except ImportError as error:
            print('Error loading module', plugin_filename, file=stderr)
            print(format_exc(), error, file=stderr)
            print('Required for step:', plugin_label, file=stderr)
            exit(2)
        if not hasattr(module, 'Plugin'):
            print("Module {} does not provide a Plugin class!".format(module), file=stderr)
            print('Required for step:', plugin_label, file=stderr)
            exit(2)
        config = validate_config(module.Plugin, plugin_label, config)
        instance = module.Plugin(config)
        instance.plugin_label = plugin_label
        instance.plugin_filename = plugin_filename
        return instance


class FilesystemLoader(CoreLoader):

    def __init__(self, core_library_path):
        self.core_library_path = normpath(core_library_path)

    def load(self, pipeline_filename, name, config, line_nr):
        """ Load a plugin based on its name """
        plugin_path = self.core_library_path.split("/")
        plugin_path.extend(name.split(" "))
        plugin_module_name = '.'.join(plugin_path)
        plugin_instance = CoreLoader().load(plugin_module_name, pipeline_filename, name, config, line_nr)
        return plugin_instance
