"""
Produce a text table
"""

from openpipe.pipeline.engine import ActionRuntime
from terminaltables import SingleTable


class Action(ActionRuntime):

    category = "Data Analysis"

    # The default behavior is to print the input item
    required_config = """
    header:     # List of labels to be used as column headers
    keys:       # List of keys to be used or row elements
    """

    def on_start(self, config):
        self.table_data = [config["header"]]

    def on_input(self, item):
        table_data = self.table_data
        if isinstance(item, list):
            for row in item:
                row_data = []
                for key in self.config["keys"]:
                    row_data.append(row[key])
                table_data.append(row_data)
            table = SingleTable(table_data)
            self.table_data = []
            self.put(table.table)
        else:
            row_data = []
            for key in self.config["keys"]:
                row_data.append(item[key])
        table_data.append(row_data)

    def on_finish(self, reason):
        if len(self.table_data) > 1:
            table = SingleTable(self.table_data)
            self.put(table.table)
