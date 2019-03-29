"""
Send a copy of the input item to other segment(s)
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Control"

    required_config = """
    name:               # Name or list of of segments to receive the item
    """

    optional_config = """
    when:   ""  # An expression that should result in a boolean

    # If `when` is set, item will only be copied to the segment(s)
    # when it evaluates to True. And sent to next action when it evaluates
    # to False
    """

    def on_start(self, config):

        # Handle single segment or list of segments
        target = config["name"]
        self.target_segments = []
        if isinstance(target, str):
            segment_list = [target]
        else:
            segment_list = target
        for segment_name in segment_list:
            target_segment = self.segment_linker(segment_name)
            self.target_segments.append(target_segment)

        if config["when"] != "":
            self.on_input = self.on_input_conditional

    def on_input(self, item):
        self.send_to_all_targets(item)
        self.put(item)

    def on_input_conditional(self, item):
        if self.config["when"]:
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
