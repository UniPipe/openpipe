"""
Duplicate input item to another segment
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_some_config = """
    Requires a segment name, or list of segment names
    """

    def on_start(self, config, segment_resolver):
        self.target_segments = []
        if isinstance(config, str):
            segment_list = [config]
        else:
            segment_list = config
        for segment_name in segment_list:
            target_segment = segment_resolver(segment_name)
            self.target_segments.append(target_segment)

    def on_input(self, item):
        for target_segment in self.target_segments:
            if isinstance(item, (list, dict)):
                new_item = item.copy()
            else:
                new_item = item
            self.put_target(new_item, target_segment)
        self.put(item)

    def on_complete(self):
        for target_segment in self.target_segments:
            self.put_target(None, target_segment)
