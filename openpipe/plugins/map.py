from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        new_item = item.copy()
        for target_field_name, target_rule in self.config.items():
            for source_field_name, source_map in target_rule.items():
                for source_value, target_value in source_map.items():
                    target_value = source_map.get(item[source_field_name])
                    if target_value is not None:
                        new_item[target_field_name] = target_value
        self.put(new_item)
