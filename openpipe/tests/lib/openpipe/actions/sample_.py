from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):
    def on_input(self, item):
        print("SAMPLE TEST LIB", self.config)
