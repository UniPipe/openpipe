"""
This is a single threaded DPL runtime engine
"""
from sys import stderr
from time import time
from ..core import PipelineRuntimeCore


class PipelineRuntime(PipelineRuntimeCore):

    def add_step_cb(self, segment_name, step_name, step_config, step_line_nr):
        """ Create a single instance of a plugin and add it to the step_list """
        step_list = self.segments.setdefault(segment_name, [])
        comp_instance = self.load_plugin(step_name, step_config, step_line_nr)
        step_list.append(comp_instance)
        comp_instance._segment_references = step_config if step_name == 'copy to segment' else []

    def create_links(self):
        """ Create links between consecutive steps and on segment references
        In a simple single threaded pipeline, the link is just a memory reference """

        # Links for consecutive steps for each segment
        for key, value in self.segments.items():
            step_list = value
            for i, step in enumerate(step_list[:-1]):
                step.next_step = step_list[i+1]

        for key, value in self.segments.items():
            step_list = value
            for i, step in enumerate(step_list):
                # print(step._segment_references)
                for reference_item in step._segment_references:
                    segment = self.segments[reference_item]
                    step.extra_steps.append(segment[0])

    def start(self):
        for segment_name, step_list in self.segments.items():
            for step in step_list:
                on_start_func = getattr(step, 'on_start', None)
                if on_start_func:
                    try:
                        on_start_func(step.initial_config)
                    except:  # NOQA: E722
                        print("Failed starting", step.plugin_label, file=stderr)
                        raise

    def activate(self):
        self.start_segment[0]._on_input(time())  # Send current time to the firs step to activate it
        self.start_segment[0]._on_input(None)    # Send end-of-input «None» to trigger on_finnish()
        return 0, None
