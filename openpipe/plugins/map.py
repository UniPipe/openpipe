from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        # Config starts with target key names, and source map rules
        for target_key_name, source_map_rule in self.config.items():
            # Source map rules provides the source_key_name and associated source_values_map
            for source_key_name, source_values_map in source_map_rule.items():
                # Check if the source value is found on the source_values map
                target_value = source_values_map.get(item[source_key_name])
                # Insert/replace value with the map target value
                if target_value is not None:
                    item[target_key_name] = target_value
        self.put(item)
