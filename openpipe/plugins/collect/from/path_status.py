"""
Produce a path status information
"""
from openpipe.engine import PluginRuntime
from os import stat
from os.path import abspath


class Plugin(PluginRuntime):

    optional_config = """
    $_$         # Path of the file to be checked
    """

    def on_input(self, item):
        path = self.config
        try:
            path_stat = stat(path)
        except FileNotFoundError:
            self.put({})
        else:
            stat_fields = [st for st in dir(path_stat) if st.startswith('st_')]
            stat_item = {}
            for st_field in stat_fields:
                stat_item[st_field[3:]] = getattr(path_stat, st_field)
            stat_item['abspath'] = abspath(path)
            self.put(stat_item)
