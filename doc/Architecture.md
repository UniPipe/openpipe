## Pipeline Loading

### Document Loader

The `DocumentLoader` class provides the following methods:
```python
class DocumentLoader:

    def get(self, document_name):
        """ Get a document content by name """

    def validate(self):
        """
        1. Transform document text to YAML
        2. Validate the YAML matches the pipeline document format
        """

    def load(self, pipeline_runtime):
        """ Load the document into runtime """
        ...
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