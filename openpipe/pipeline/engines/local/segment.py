from os import environ
from openpipe.utils import plugin_load
from time import time
from sys import stderr

DEBUG = environ.get("DEBUG")


class PipelineSegment:
    def __init__(self, segment_name):
        self.segment_name = segment_name
        self.action_list = []
        self.config_list = []

    def add(self, action_name, action_config, action_label):
        action_instance = plugin_load(action_name, action_config, action_label)
        self.action_list.append(action_instance)
        self.config_list.append(action_config)

    def activate(self, activation_item=True):
        self.action_list[0].reference_count = 1
        self.action_list[0]._on_input(
            time()
        )  # Send current time to the firs action to activate it
        self.action_list[0]._on_input(
            None
        )  # Send end-of-input «None» to trigger on_finnish()
        return 0, None  # exit code, exit message

    def start(self, _segment_linker):
        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    print("on_start %s " % action.plugin_label)
                try:
                    action.segment_linker = _segment_linker
                    on_start_func(action.initial_config)
                    action.segment_linker = None
                except:  # NOQA: E722
                    print("Failed starting", action.plugin_label, file=stderr)
                    raise


class SegmentManager:
    def __init__(self):
        self._segments = {}

    def start(self):
        """ Runs the start code for every segment created on this manager """
        for segment_name, segment in self._segments.items():
            segment.start(self._segment_linker)

    def create(self, segment_name):
        segment = PipelineSegment(segment_name)
        self._segments[segment_name] = segment
        return segment

    def activate(self, start_segment_name="start"):
        return self._segments[start_segment_name].activate()

    def _segment_linker(self, segment_name):
        """ Returns a reference name to a local segment """
        try:
            segment = self._segments[segment_name]
        except KeyError:
            print(
                "A reference was found for segment '{}' which does not exist.\n"
                "The following segment names were found:\n{}\n\n".format(
                    segment_name, list(self.segments.keys())
                ),
                file=stderr,
            )
            exit(2)

        segment.action_list[0].reference_count += 1
        return segment.action_list[0]

    def create_action_links(self):
        """ Create links between consecutive action and on segment references
        In a simple single threaded pipeline, the link is just a memory reference """

        # Links for consecutive steps for each segment
        for segment_name, segment in self._segments.items():
            action_list = segment.action_list
            # Create links to next on all actions  except for the last
            for i, action in enumerate(action_list[:-1]):
                action.next_action = action_list[i + 1]
                action_list[i + 1].reference_count += 1
