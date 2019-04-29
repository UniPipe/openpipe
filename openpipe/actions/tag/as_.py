"""
Tag the input value using tag key
"""

from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    category = "Data Control"

    required_config = """
    tag_key_name:     #  Default is to tag the entire input item
    """

    def on_input(self, item):
        new_tag = {self.config["tag_key_name"]: item}
        current_tag = self._tag or {}
        self.set_tag({**current_tag, **new_tag})
        self.put(item)
