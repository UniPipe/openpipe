"""
Produce the list of files matching a pattern
"""
from openpipe.pipeline.engine import ActionRuntime
from pathlib import Path


class Action(ActionRuntime):

    category = "Data Sourcing"

    optional_config = """
    $_$     # The pattern to be used for matching
    """

    def on_input(self, item):
        path = Path(self.config).expanduser().as_posix()
        # Because PathLib's glob() does not support absolute patterns
        # Transform them into a relative pattern to "/"
        if path[0] == "/":
            root_path = "/"
            pattern = path[1:]
        else:
            root_path = "."
            pattern = path
        file_list = sorted(Path(root_path).glob(pattern))
        file_list = [filename.as_posix() for filename in file_list]
        self.put(file_list)
