"""
Send item to other pipeline depending on a condition
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    segment:        # Name of segment to receive the item if `on_condition` is True
    on_condition:   # Expression to be evaluated
    """

    def on_start(self, config):
        self.send_to_target = self.segment_resolver(config['segment'])

    def on_input(self, item):
        if self.config['on_condition']:
            self.put_target(item, self.send_to_target)
        else:
            self.put(item)

    def on_finish(self, reason):
        self.put_target(None, self.send_to_target)
