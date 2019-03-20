# This module provides just a reference to the default runtime, so
# that in the future it can be extended to support runtime selection

from .engines.local import PipelineManager
from .engines.local import PluginRuntime

__all__ = [
    PipelineManager,
    PluginRuntime
]
