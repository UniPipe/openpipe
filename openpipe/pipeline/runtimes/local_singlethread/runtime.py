from openpipe.core import plugin_load


class PipelineRuntime:

    class PipelineSegment:
        def __init__(self, segment_name):
            self.segment_name = segment_name
            self.action_list = []

        def add(self, action_name, action_config, action_label):
            action_instance = plugin_load(action_name, action_config, action_label)
            self.action_list.append(action_instance)

    def create_segment(self, segment_name):
        return self.PipelineSegment(segment_name)

    def start(self):
        pass

    def create_action_links(self):
        pass

    def activate(self):
        pass

    def load_plugin(step_name, step_params, step_line_nr):
        pass

    def load(self, plugin_filename, pipeline_filename, name, params, line_nr):
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
        params = validate_params(module.Plugin, plugin_label, params)
        instance = module.Plugin(params)
        instance.plugin_label = plugin_label
        instance.plugin_filename = plugin_filename
        return instance