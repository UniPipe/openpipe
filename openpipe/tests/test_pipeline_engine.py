from openpipe.client import PipelineFileLoader
from openpipe.pipeline.engine import PipelineManager


def test_runtime_run():

    # Load and validate file syntax
    pipeline_loader = PipelineFileLoader()
    pipeline_loader.fetch("samples/test.yaml")
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
    activation_item = {"name": "samples/test.yaml", "arguments": ()}
    pipeline_manager.activate(activation_item)
