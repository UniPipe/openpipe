"""
"""
from openpipe.utils.yaml_extra import load_yaml, remove_line_info
from sys import stderr
from pprint import pformat

SEGMENTS_DOC_URL = "https://www.openpipe.org/1.0/language/#segments"


class PipelineLoader:
    def fetch(self, pipeline_name):
        self._name = pipeline_name
        self._document_data = self.get(pipeline_name)
        self._document_dict = {}

    def validate(self, start_segment="start", document_name=None):
        """
        1. Transform document text to YAML
        2. Validate the YAML matches the pipeline document format
        """
        if document_name:
            document_data = self.get(document_name)
        else:
            document_data = self._document_data
        python_data = load_yaml(document_data)
        self.start_segment = start_segment

        if not isinstance(python_data, dict):
            if document_name:
                print("Loading file %s" % document_name, file=stderr)
            print(
                "Pipeline YAML must start with a dictionary !\n"
                "Instead got:\n{}\n".format(pformat(python_data))
                + "You can read more about the segments format at:\n"
                + SEGMENTS_DOC_URL,
                file=stderr,
            )
            exit(1)

        # We don't need the __line__ info for the top level dict
        del python_data["__line__"]

        # A single segment was provided
        if start_segment not in python_data:
            available_segment_names = list(python_data.keys())
            if document_name:
                print("Loading file %s" % document_name, file=stderr)
            print(
                "Start segment '{}' was not found\n"
                "The following segment names were found:\n{}\n\n".format(
                    start_segment, available_segment_names
                )
                + "You can read more about pipeline segments at:\n"
                + SEGMENTS_DOC_URL,
                file=stderr,
            )
            exit(1)

        for segment_name, action_sequence in python_data.items():
            if segment_name[0] == "_":
                continue

            if not isinstance(action_sequence, list):
                if document_name:
                    print("Loading file %s" % document_name, file=stderr)
                print(
                    "The content of segment '{}' is not a sequence as expected.\n".format(
                        segment_name
                    )
                    + "Instead got:\n{}\n\n".format(python_data[segment_name])
                    + "You can read more about pipeline segments at:\n"
                    + SEGMENTS_DOC_URL,
                    file=stderr,
                )
                exit(1)

            for action in action_sequence:
                if not isinstance(action, dict):
                    if document_name:
                        print("Loading file %s" % document_name, file=stderr)
                    print(
                        "ERROR on file \"{}\", segment '{}:'\n".format(
                            self._name, segment_name
                        )
                        + "Expected action defined as dictionary, got {} '{}'\n\n".format(
                            type(action), action
                        )
                        + "You can read more about pipeline segments at:\n"
                        + SEGMENTS_DOC_URL,
                        file=stderr,
                    )
                    exit(2)

        if document_name:
            return python_data
        else:
            self._document_dict = python_data

    def load(self, pipeline_manager, document_dict=None, calling_id=None):
        document_dict = document_dict or self._document_dict
        """ Load the document into a pipeline runtime """
        libraries = document_dict.get("_libraries")
        if libraries:
            del document_dict["_libraries"]
            for library in libraries:
                pipeline_manager.load_library(library)

        for segment_name, action_list in document_dict.items():
            if calling_id:
                segment_name += "_" + calling_id
            # segments with a leading _ can be used as config placeholders
            if segment_name[0] == "_":
                continue

            segment_manager = pipeline_manager.create_segment(segment_name)
            for action in action_list:
                line_nr = action["__line__"]
                remove_line_info(action)
                action_name, action_config = next(iter(action.items()))
                caller_id = 'file "{}", line {}'.format(self._name, line_nr)
                if action_name == "send to pipeline":
                    pipeline_name = action_config
                    sub_document_dict = self.validate("start", pipeline_name)
                    self.load(pipeline_manager, sub_document_dict, caller_id)
                    sub_start_segment = "start" + "_" + caller_id
                    action_name = "send to segment"
                    action_config = sub_start_segment
                elif calling_id and action_name == "send to segment":
                    action_config = self._rename_segments(action_config, calling_id)
                action_label = "'{}', file \"{}\", line {}".format(
                    action_name, self._name, line_nr
                )
                segment_manager.add(action_name, action_config, action_label)

    def _rename_segments(self, action_config, calling_id):
        """ return segment names postfixed with the callind_id """

        if isinstance(action_config, str):
            return action_config + "_" + calling_id
        if isinstance(action_config, list):
            return [segment_name + "_" + calling_id for segment_name in action_config]
        raise NotImplementedError

    def get(self, document_name):
        """ Get a document content by name """
        # Add here the code required to load a document by name
        raise NotImplementedError
