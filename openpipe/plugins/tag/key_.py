"""
Tag a key or list of keys
# Tagged keys will be stored as _tag[key] = [tem(key]
"""

from openpipe.pipeline.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_config = """
    key_list:     #  The list of data keys to be tagged
    """

    def on_input(self, item):
        current_tag = self._tag or {}

        key_list = self.config['key_list']
        if not isinstance(key_list, list):
            key_list = [key_list]

        new_tag = {}
        for key in key_list:
            new_tag[key] = item[key]
        # Python 3.x syntax for dict merging
        self.set_tag({**current_tag, **new_tag})
        self.put(item)
