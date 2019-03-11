from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    def on_input(self, item):
        print("SAMPLE TEST LIB", self.config)
