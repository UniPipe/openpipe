"""
Produce the input items sorted by keys
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    requiredl_params = """
    key:                    # Expression to be used as the group key
    """

    optional_params = """
    descendent: False       # Use descendent order ?
    """

    def on_start(self, params):
        self.data = []
        self.descendent = params['descendent']

    def on_input(self, item):
        # we must copy because the item may be changed in the thread
        self.data.append((self.params['key'], item.copy()))

    def on_finish(self, reason):
        self.data.sort(key=lambda x: x[0], reverse=self.descendent)
        for key, item in self.data:
            self.put(item)
