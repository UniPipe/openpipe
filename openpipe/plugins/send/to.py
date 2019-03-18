"""
Send a copy of the input item to other segment(s)
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    segment:            # Name or list of of segments to receive the item
    """

    optional_config = """
    on_condition:   ""  # An expression that should result in a boolean

    # If `on_condition` is set, item will only be copied to the segment(s)
    # when it evaluates to True. And sent to next step when it evaluates
    # to False
    """

    def on_start(self, config):

        # Handle single segment or list of segments
        target = config['segment']
        self.target_segments = []
        if isinstance(target, str):
            segment_list = [target]
        else:
            segment_list = target
        for segment_name in segment_list:
            target_segment = self.segment_resolver(segment_name)
            self.target_segments.append(target_segment)

        if config['on_condition'] != "":
            self.on_input = self.on_input_conditional

    def on_input(self, item):
        if self.config['on_condition']:
            self.put_target(item, self.send_to_target)
        else:
            self.put(item)

    def on_input_conditional(self, item):
        if self.config['on_condition']:
            self.send_to_all_targets(item)
        else:
            self.put(item)

    def on_finish(self, reason):
        self.send_to_all_targets(None)

    def send_to_all_targets(self, item):
        for target_segment in self.target_segments:
            if isinstance(item, (list, dict)):
                new_item = item.copy()
            else:
                new_item = item
        self.put_target(new_item, target_segment)
