from openpipe.core import PipelineLoader


class PipelineFileLoader(PipelineLoader):

    def get(self, pipeline_name):
        with open(pipeline_name) as document_file:
            return document_file.read()
