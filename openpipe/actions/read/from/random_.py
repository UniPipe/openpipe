"""
Generate a random number
"""
from openpipe.pipeline.engine import ActionRuntime
from random import seed, randint
from functools import partial


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_some_config = """
    The max number that can be generated.
    Generated numbers will be between 0 and max number.
    """

    def on_start(self, config):
        seed()
        if isinstance(config, dict):
            random_dict = self.random_dict = {}
            for key, value in config.items():
                random_dict[key] = self.random_function(value)
            self.on_input = self.on_input_dict
        else:
            self.random_func = self.random_function(config)

    # Output a random number
    def on_input(self, item):
        self.put(self.random_func())

    def on_input_dict(self, item):
        new_item = {}
        for key, random_func in self.random_dict.items():
            new_item[key] = random_func()
        self.put(new_item)

    @staticmethod
    def random_function(random_spec):
        """ Return a function that provides the feature described by random_spec """
        if isinstance(random_spec, int):
            return partial(randint, 0, random_spec)
        if isinstance(random_spec, str):
            start, end = random_spec.split("..")
            return partial(randint, int(start), int(end))
