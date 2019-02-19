from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_start(self, config, segment_resolver):
        self.send_to_target = segment_resolver(config['send to'])

    def on_input(self, item):
        if self.config['on condition']:
            self.put_target(item, self.send_to_target)
        else:
            self.put(item)

    def on_complete(self):
        self.put_target(None, self.send_to_target)
