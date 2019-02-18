"""
"""
from .yaml import load_yaml, remove_line_info
from sys import stderr

SEGMENTS_DOC_URL = "https://www.openpipe.org/OpenPipeLanguage#Segment"


class PipelineDocument(object):

    def __init__(self, filename=None, yaml_data=None, start_segment='start', on_step_cb=None, load_libraries_cb=None):
        self.on_step_cb = on_step_cb
        self.load_libraries_cb = load_libraries_cb
        if filename:
            with open(filename, 'r') as data_file:
                self.yaml_data = data_file.read()
        else:
            self.yaml_data = yaml_data
        self.start_segment = start_segment

    def load(self):  # NOQA: C901
        loaded_segments = []
        referred_segments = []
        python_data = load_yaml(self.yaml_data)

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

        segment_names = list(python_data.keys())

        # A single segment was provided
        start_segment = self.start_segment
        if start_segment not in python_data:
            print(
                "Start segment '{}' was not found\n"
                "The following segment names were found:\n{}\n\n".format(start_segment, segment_names) +
                "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                file=stderr
                )
            exit(1)
        referred_segments.append(start_segment)
        while len(referred_segments) > 0:
            segment_name = referred_segments.pop(0)
            try:
                step_list = python_data[segment_name]
            except KeyError:
                print(
                    "A reference was found for segment '{}' which does not exist."
                    "The following segment names were found:\n{}\n\n".format(segment_name, segment_names) +
                    "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                    file=stderr
                    )
                exit(2)
            loaded_segments.append(segment_name)

            if not isinstance(step_list, list):
                print(
                    "The content of segment '{}' is not a sequence as expected.\n".format(segment_name) +
                    "Instead got:\n{}\n\n".format(python_data[segment_name]) +
                    "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                    file=stderr
                    )
                exit(1)

            for step in step_list:
                if not isinstance(step, dict):
                    print(
                        "ERROR on segment '{}'\n".format(start_segment) +
                        "Expected a step definition in the format 'key: value', got '{}'\n\n".format(step) +
                        "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                        file=stderr
                    )
                    exit(2)
                step_name, step_config = list(step.items())[0]
                step_line_nr = step['__line__']
                remove_line_info(step_config)

                if step_name == 'copy to segment':
                    possible_segments = step_config
                    for name in possible_segments:
                        if name not in loaded_segments and name not in referred_segments:
                            referred_segments.append(name)

                if step_name == 'test':
                    on_true_segment = step_config.get('on_true', [])
                    on_false_segment = step_config.get('on_false', [])
                    for name in [on_true_segment, on_false_segment]:
                        if name not in loaded_segments and name not in referred_segments:
                            referred_segments.append(name)

                if self.on_step_cb:
                    self.on_step_cb(segment_name, step_name, step_config, step_line_nr)
