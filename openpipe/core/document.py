"""
"""
from .yaml import load_yaml, remove_line_info
from sys import stderr

SEGMENTS_DOC_URL = "https://www.openpipe.org/OpenPipeLanguage#Segment"


class PipelineLoader:

    def fetch(self, pipeline_name):
        self._name = pipeline_name
        self._document_data = self.get(pipeline_name)
        self._document_dict = {}

    def validate(self, start_segment="start"):
        """
        1. Transform document text to YAML
        2. Validate the YAML matches the pipeline document format
        """
        python_data = load_yaml(self._document_data)

        if not isinstance(python_data, dict):
            print(
                "The provided YAML does not provide any segment (key: content).\n"
                "Instead got:\n{}\n".format(python_data) +
                "You can read more about the segments format at:\n"+SEGMENTS_DOC_URL,
                file=stderr
                )
            exit(1)

        # We don't need the __line__ info for the top level dict
        del python_data['__line__']

        libraries = python_data.get('libraries')
        if libraries:
            del python_data['libraries']
            if self.load_libraries_cb:
                self.load_libraries_cb(list(libraries))

        # A single segment was provided
        if start_segment not in python_data:
            available_segment_names = list(python_data.keys())
            print(
                "Start segment '{}' was not found\n"
                "The following segment names were found:\n{}\n\n".format(start_segment, available_segment_names) +
                "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                file=stderr
                )
            exit(1)

        for segment_name, action_sequence in python_data.items():
            if segment_name[0] == "_":
                continue

            if not isinstance(action_sequence, list):
                print(
                    "The content of segment '{}' is not a sequence as expected.\n".format(segment_name) +
                    "Instead got:\n{}\n\n".format(python_data[segment_name]) +
                    "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                    file=stderr
                    )
                exit(1)

            for action in action_sequence:
                if not isinstance(action, dict):
                    print(
                        "ERROR on segment '{}'\n".format(segment_name) +
                        "Expected a step definition in the format 'key: value', got '{}'\n\n".format(action) +
                        "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                        file=stderr
                    )
                    exit(2)

        self._document_dict = python_data

    def load(self, pipeline_runtime):
        """ Load the document into a pipeline runtime """

        libraries = self._document_dict.get('libraries')
        if libraries:
            del self._document_dict['libraries']
            for library in libraries:
                pipeline_runtime.load_library(library)

        for segment_name, action_list in self._document_dict.items():
            # segments with a leading _ can be used as config placeholders
            if segment_name[0] == "_":
                continue
            segment_manager = pipeline_runtime.create_segment(segment_name)
            for action in action_list:
                line_nr = action['__line__']
                remove_line_info(action)
                action_name, action_config = next(iter(action.items()))
                action_label = "'{}', file \"{}\", line {}".format(action_name, self._name, line_nr)
                segment_manager.add(action_name, action_config, action_label)

    def get(self, document_name):
        """ Get a document content by name """
        # Add here the code required to load a document by name
        raise NotImplementedError



