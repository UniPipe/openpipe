"""
Update values depending on conditional expressions
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Manipulation"

    required_config = """
    set:            # Dictionary with keys/values to be updated
    """
    optional_config = """
    where:  True    # Expression to select items to be updated
    else:   {}      # Dictionary with keys/values to be updated when 'where' is False
    """

    def on_input(self, item):
        new_item = item
        where = self.config["where"]
        if where is True:
            for key, value in self.config["set"].items():
                new_item[key] = value
        if where is False:
            for key, value in self.config["else"].items():
                new_item[key] = value
        self.put(new_item)
