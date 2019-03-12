"""
Retrieve a file from a FTP server into a local destination
"""
from openpipe.engine import PluginRuntime
# from urllib.request import urlretrieve


class Plugin(PluginRuntime):

    def on_input(self, item):
        pass
        # source = self.config['source']
        # destination = self.config['destination']
        # urlretrieve(source, destination)
        # self.put(destination)
