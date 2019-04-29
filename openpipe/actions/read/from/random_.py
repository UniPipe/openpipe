"""
Generate a random number
"""
from openpipe.pipeline.engine import ActionRuntime
from random import seed, randint


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The max number that can be generated.
    Generated numbers will be between 0 and max number.
    """

    def on_start(self, config):
        seed()

    # Output a random number
    def on_input(self, item):
        self.put(randint(0, self.config))
