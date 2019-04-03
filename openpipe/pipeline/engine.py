# Load the engine specific managers and runtimes

from importlib import import_module
from os import environ

engine_name = ".engines." + environ.get("OPENPIPE_ENGINE", "local")

engine_package = import_module(engine_name, "openpipe.pipeline")
PipelineManager = engine_package.PipelineManager
ActionRuntime = engine_package.ActionRuntime

__all__ = [PipelineManager, ActionRuntime]
