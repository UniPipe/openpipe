from openpipe.core import DocumentLoader
from openpipe.engine import PipelineRuntime


def test_runtime_runt():
    document = DocumentLoader().get('test.yaml')
    document.validate()
    runtime = PipelineRuntime()
    # Document is loaded into a pipeline runtime
    document.load(runtime)
    runtime.start()
    runtime.create_action_links()
    runtime.activate()
