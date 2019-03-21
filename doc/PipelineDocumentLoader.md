## Openpipe Architecture


The _Document Loader_ must be a Python class  derived from `openpipe.client.PipelineLoader` and it must implement the `get(self, pipeline_name)` method. This method is used to load a pipeline document based on it's name.

Openpipe includes a base loaders, the `openpipe.client.FileDocumentLoader` which will consider the name as a local filename, and open it.