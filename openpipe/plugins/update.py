"""
Update parts of input item
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_start(self, config, segment_resolver):
        if isinstance(config, dict) and 'set' in config:
            pass
        else:
            raise ValueError("The update plugin config must have a 'set' key ")

    # Output the configuration item
    def on_input(self, item):
        new_item = item
        where = self.config.get('where', True)
        if where is True:
            if isinstance(self.config['set'], dict):
                for key, value in self.config['set'].items():
                    new_item[key] = value
            else:
                new_item = self.config['set']
        if where is False and 'else' in self.config:
            if isinstance(self.config['else'], dict):
                for key, value in self.config['else'].items():
                    new_item[key] = value
            else:
                new_item = self.config['else']
        self.put(new_item)
