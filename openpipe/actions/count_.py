"""
Count the number of elements received
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Analysis"

    optional_config = """
    group_by:   ""  # Expression to use for count aggregation
    """

    def on_start(self, config):
        if config["group_by"] == "":  # Simple per input count
            self.count = 0
        else:
            self.count_dict = {}
            self.on_input = self.on_input_group_by

    def on_input(self, item):
        self.count += 1
        self.put(self.count)

    def on_input_group_by(self, item):
        group_by = self.config["group_by"]
        try:
            count = self.count_dict[group_by]
        except KeyError:
            count = 0
        count += 1
        self.count_dict[group_by] = count

    def on_finish(self, reason):
        if hasattr(self, "count_dict"):
            new_item = {}
            for key, value in self.count_dict.items():
                new_item[key] = value
            # If no items were received, don't trigger results
            if new_item:
                self.put(new_item)
