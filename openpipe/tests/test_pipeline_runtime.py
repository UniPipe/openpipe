from openpipe.pipeline.loaders import PipelineFileLoader
from openpipe.pipeline.runtime import PipelineRuntime

from os.path import join


def test_runtime_runt():

    doc_loader = PipelineFileLoader()
    test_filename = join('samples', 'test.yaml')
    doc_loader.fetch(test_filename)
    doc_loader.validate()

    runtime = PipelineRuntime()

    # Document is loaded into a pipeline runtime
    doc_loader.load(runtime)

    runtime.start()
    runtime.create_action_links()
    runtime.activate()
