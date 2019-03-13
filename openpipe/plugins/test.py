"""
Send item to different pipeline depending on_condition value
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    on_condition:   # Expression to be evaluated
    send_to:        # Name of segment to receive the item if `on_condition` is True
    """

    def on_start(self, config, segment_resolver):
        self.send_to_target = segment_resolver(config['send_to'])

    def on_input(self, item):
        if self.config['on_condition']:
            self.put_target(item, self.send_to_target)
        else:
            self.put(item)

    def on_complete(self):
        self.put_target(None, self.send_to_target)
