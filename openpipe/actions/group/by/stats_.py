"""
Produce statistics by grouping input items by keys
"""
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Analysis"

    required_config = """
    keys:         # List of keys to be used for grouping
    """

    optional_config = """
    stats: [sum, count, max, min]   # List of stats to obtain
    sorted_fields: []               # When these fields change, produce the sort
    """

    def on_start(self, config):
        self.group_by = GroupBy(self, config)

    def on_input(self, item):
        self.group_by.add(item)

    def on_finish(self, reason):
        self.group_by.send_group_results()


def group_sum(current_value, new_value):
    return current_value + new_value


def group_count(current_value, new_value):
    return current_value + 1


def group_max(current_value, new_value):
    return max(current_value, new_value)


def group_min(current_value, new_value):
    return min(current_value, new_value)


STATS_FUNCS = {
    "sum": group_sum,
    "count": group_count,
    "max": group_max,
    "min": group_min,
}


class GroupBy(object):
    def __init__(self, action, config):
        self.config = config
        self.last_sorted_value = None
        self.sorted_fields = config["sorted_fields"]
        self.stats_fields = config["stats"]
        self.action = action
        self.aggregated_stats = {}

    def add(self, item):

        # Create composed aggregation with the values of config fields
        group_key = "\n".join(item[x] for x in self.config["keys"])

        # if using "sorted_fields", sent results when the result key changes
        if self.sorted_fields:
            current_sorted_value = list(map(lambda x: item[x], self.sorted_fields))
            if self.last_sorted_value != current_sorted_value:
                if self.last_sorted_value is not None:
                    self.send_group_results()
                self.last_sorted_value = current_sorted_value

        # Update aggregation results

        # If dict for group_key is empty, initialize it
        group = self.aggregated_stats.get(group_key, {})
        if group == {}:
            self.aggregated_stats[group_key] = group

        # Create a dict for each field
        for stats_field_name in self.stats_fields:
            item_value = item[stats_field_name]
            # If dict for stats_field_name is empty, initialize it
            field_stats = group.get(stats_field_name, {})
            if field_stats == {}:
                group[stats_field_name] = field_stats
            # Create a dict item for each aggregation function
            for func_name, func in STATS_FUNCS.items():
                if func in [group_min, group_max]:
                    current_value = item_value
                else:
                    current_value = 0
                current_value = field_stats.get(func_name, current_value)
                field_stats[func_name] = func(current_value, item_value)

    def send_group_results(self):
        if self.aggregated_stats == {}:
            return
        new_item = {}
        for group_key, stats in self.aggregated_stats.items():

            # Add the group_by field values
            group_values = group_key.split("\n")
            for i, field_name in enumerate(self.config["keys"]):
                new_item[field_name] = group_values[i]

            # Add stats results
            for stats_field_name, func_results in stats.items():
                for func_name, result in func_results.items():
                    new_item[stats_field_name + "_" + func_name] = func_results[
                        func_name
                    ]
                new_item[stats_field_name + "_avg"] = (
                    float(func_results["sum"]) / func_results["count"]
                )
            self.action.put(new_item)
        self.aggregated_stats = {}
