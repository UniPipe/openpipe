from openpipe.core import PipelineLoader
from os.path import normpath


class PipelineFileLoader(PipelineLoader):

    def get(self, pipeline_name):
        pipeline_name = normpath(pipeline_name)
        with open(pipeline_name) as document_file:
            return document_file.read()


class PipelineStringLoader(PipelineLoader):

    def get(self, pipeline_string):
        pipeline_string = "string_loader"
        return pipeline_string
