"""
This is a single threaded DPL runtime engine
"""
from sys import stderr
from os import environ
from time import time
from ..core import PipelineRuntimeCore

SEGMENTS_DOC_URL = "https://www.openpipe.org/OpenPipeLanguage#Segment"
ODP_RUNTIME_DEBUG = environ.get('ODP_RUNTIME_DEBUG')


class PipelineRuntime(PipelineRuntimeCore):

    def add_step_cb(self, segment_name, step_name, step_config, step_line_nr):
        """ Create a single instance of a plugin and add it to the step_list """
        step_list = self.segments.setdefault(segment_name, [])
        plugin_instance = self.load_plugin(step_name, step_config, step_line_nr)
        step_list.append(plugin_instance)

    def create_links(self):
        """ Create links between consecutive steps and on segment references
        In a simple single threaded pipeline, the link is just a memory reference """

        # Links for consecutive steps for each segment
        for key, value in self.segments.items():
            step_list = value
            for i, step in enumerate(step_list[:-1]):
                step.next_step = step_list[i+1]
                step_list[i+1].reference_count += 1

    def segment_resolver(self, segment_name):
        try:
            first_step = self.segments[segment_name][0]
        except KeyError:
            print(
                "A reference was found for segment '{}' which does not exist."
                "The following segment names were found:\n{}\n\n".format(segment_name, self.segments) +
                "You can read more about pipeline segments at:\n"+SEGMENTS_DOC_URL,
                file=stderr
                )
            exit(2)
        first_step.reference_count += 1
        return first_step

    def start(self):
        for segment_name, step_list in self.segments.items():
            for step in step_list:
                on_start_func = getattr(step, 'on_start', None)
                if on_start_func:
                    if ODP_RUNTIME_DEBUG:
                        print("on_start %s " % step.plugin_label)
                    try:
                        on_start_func(step.initial_config, self.segment_resolver)
                    except:  # NOQA: E722
                        print("Failed starting", step.plugin_label, file=stderr)
                        raise

    def activate(self):
        self.start_segment[0].reference_count = 1
        self.start_segment[0]._on_input(time())  # Send current time to the firs step to activate it
        self.start_segment[0]._on_input(None)    # Send end-of-input «None» to trigger on_finnish()
        return 0, None
