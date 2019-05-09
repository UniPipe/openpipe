"""
Generate a random string
"""
from openpipe.pipeline.engine import ActionRuntime
from random import seed, randint, choice


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_config = """
        charset:  # The range of chars that are allowed: a..z
        length:   # Leng of the string, variable: 10..20
    """

    def on_start(self, config):
        seed()
        charset = config['charset']
        length = config['length']
        if '..' in charset:
            start_char, end_char = charset.split("..")
            charset = [chr(x) for x in range(ord(start_char), ord(end_char))]
        if isinstance(length, str) and '..' in length:
            min_len, max_len = length.split("..")
            min_len, max_len = int(min_len), int(max_len)
        else:
            min_len = max_len = length
        self.charset = charset
        self.min_len = min_len
        self.max_len = max_len

    # Output a random string
    def on_input(self, item):
        random_str = ''
        length = randint(self.min_len, self.max_len)
        for _ in range(length):
            random_str += choice(self.charset)
        self.put(random_str)
