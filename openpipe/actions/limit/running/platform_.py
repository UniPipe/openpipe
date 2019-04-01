"""
Produce items only when running on the specified platform
"""
import platform
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Control"

    required_config = """
    system:    # The system name, e.g. 'Linux', 'Windows' 'Darwin'
    """

    def on_start(self, config):

        if platform.system() != config["system"]:
            self.on_input = self.on_input_pass

    def on_input(self, item):
        self.put(item)

    def on_input_pass(self, item):
        pass
