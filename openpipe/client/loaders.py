import io
from openpipe.client import PipelineLoader
from os.path import normpath


class PipelineFileLoader(PipelineLoader):
    def get(self, pipeline_name):
        pipeline_name = normpath(pipeline_name)
        with io.open(pipeline_name, encoding="utf8") as document_file:
            return document_file.read()


class PipelineStringLoader(PipelineLoader):
    def get(self, pipeline_string):
        pipeline_string = "string_loader"
        return pipeline_string
