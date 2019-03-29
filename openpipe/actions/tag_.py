"""
Tag input item with the provided configuration tag item
"""

from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Control"

    optional_config = """
    $_$     #  Default is to tag the entire input item
    """

    def on_input(self, item):
        if isinstance(self.config, dict):
            current_tag = self._tag or {}
            self.set_tag({**current_tag, **self.config})
        else:
            self.set_tag(item)
        self.put(item)
