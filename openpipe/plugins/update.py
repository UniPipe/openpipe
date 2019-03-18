"""
Produce the input item after updating values
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    required_params = """
    set:            # Dictionary with keys/values to be updated
    """
    optional_params = """
    where:  True    # Expression to select items to be updated
    else:   {}      # Dictionary with keys/values to be updated when 'where' is False
    """

    def on_input(self, item):
        new_item = item
        where = self.params['where']
        if where is True:
            for key, value in self.params['set'].items():
                new_item[key] = value
        if where is False:
            for key, value in self.params['else'].items():
                new_item[key] = value
        self.put(new_item)
