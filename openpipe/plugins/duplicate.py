"""
Duplicate input item to another segment
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    segment:        # Name of the segment to receive the item
    """

    optional_config = """
    when:   True    # Expression 
    else:   ''      # 
    """

    def on_start(self, config, segment_resolver):
        self.target_segment = segment_resolver(config['to segment'])

    def on_input(self, item):
        if isinstance(item, (list, dict)):
            new_item = item.copy()
        else:
            new_item = item
        self.put_target(new_item, self.target_segment)
        self.put(item)

    def on_complete(self):
        self.put_target(None, self.target_segment)
