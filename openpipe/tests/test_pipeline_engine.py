from openpipe.client import PipelineFileLoader
from openpipe.pipeline.engine import PipelineManager
from openpipe.utils import get_platform_info
from os.path import abspath, dirname
from os import environ


def test_runtime_run():

    filename = "samples/test.yaml"

    # Load and validate file syntax
    pipeline_loader = PipelineFileLoader()
    pipeline_loader.fetch(filename)
    pipeline_loader.validate()

    # Create a pipeline manager
    pipeline_manager = PipelineManager("start")

    # Load will create all the action instances into provided pipeline manager
    # using the Pipeline Manager API
    pipeline_loader.load(pipeline_manager)

    # Runs the start method of all actions
    pipeline_manager.start()

    # Create links between actions
    pipeline_manager.create_action_links()

    # Send the activation element into the pipeline
    path = abspath(dirname("samples/test.yaml"))
    activation_item = {
        "platform": get_platform_info(),
        "environment": environ.copy(),
        "path": path,
        "name": filename,
        "arguments": (),
    }
    pipeline_manager.activate(activation_item)
