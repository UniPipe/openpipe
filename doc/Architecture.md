## Openpipe Architecture

## Introduction
Openpipe is built using a modular architecture to facilitate extensibility.

- _core_
    _
- _pipeline loader_
- _pipeline engine_
    - _pipeline manager_
    - _segment manager_


The _Document Loader_ must be a Python class  derived from `openpipe.core.PipelineLoader` and it must implement the `get(self, pipeline_name)` method. This method is used to load a pipeline document based on it's name.

Openpipe includes two base loaders, the `FileDocumentLoader` which will consider the name as a local filename, and open it, and the `NetFileDocumentLoader` which extends the `FileDocumentLoader` with the ability to automatically download remote files if the name starts with _http(s):_ .

```python
class MyDocumentLoader(DocumentLoader):

    def get(self, document_name):
        """ Get a document content by name """
        # Add here the code required to load a document by name
```

### Pipeline Runtime
The pipeline runtime must provide:

```python
class PipelineRuntime:

    def create_segment(self, segment_name):
        """ Create a segment """
        ...

    def load_action(self, segment_name, action_name, action_config, action_label):
        """ Loads an action
        action_label is the label to be reported on runtime errors (document name / line number)
        map action to modules
        load module
        validate the module plugin config schema
        validate action config meets the action plugin schema
        create plugin instance
        """

    def link_to_segment(self, segment_name):
        """ Get a link to the first action of a  segment """

    def load_library(self, library_name):
        """ Loads a library """
        ...

    def start(self):
        """ Calls the start handler for all actions """

    def create_links(self):
        """ Establish links between actions in the pipeline """

    def activate(self):
        """ Deliver the activation event to the first action """

```


## ResourceLoader

## ActionMapper
The ActionMapper maps names to python modules

Action
    Parameters