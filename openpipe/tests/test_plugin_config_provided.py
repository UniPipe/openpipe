from openpipe.pipeline.engine import PluginRuntime
from openpipe.core.plugin_config import validate_provided_config


def test_zero_config():
    class Plugin(PluginRuntime):
        pass

    validate_provided_config(Plugin, __file__, None)
