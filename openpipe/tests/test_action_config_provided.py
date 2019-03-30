from openpipe.pipeline.engine import ActionRuntime
from openpipe.utils.action_config import validate_provided_config


def test_zero_config():
    class Action(ActionRuntime):
        pass

    validate_provided_config(Action, __file__, None)
