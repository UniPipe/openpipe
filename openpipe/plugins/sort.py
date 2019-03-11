"""
Sort input items by key
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    # By default sort full element

    def on_start(self, config, segment_resolver):
        self.data = []
        self.descendent = config.get("descendent", False)

    def on_input(self, item):
        # we must copy because the item may be changed in the thread
        self.data.append((self.config['key'], item.copy()))

    def on_complete(self):
        self.data.sort(key=lambda x: x[0], reverse=self.descendent)
        for key, item in self.data:
            self.put(item)
