""" This module provides the segment management classes """

from os import environ
from openpipe.utils import create_action_instance
from sys import stderr
from wasabi import Printer

DEBUG = environ.get("DEBUG")


class PipelineSegment:
    def __init__(self, segment_name):
        self.segment_name = segment_name
        self.action_list = []
        self.config_list = []

    def add(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label
        )
        self.action_list.append(action_instance)
        self.config_list.append(action_config)

    def activate(self, activate_arguments):
        self.action_list[0].input_sources.append(self)
        self.action_list[0]._on_input(
            self, activate_arguments, None
        )  # Send current time to the firs action to activate it
        self.action_list[0]._on_input(
            self, None, None
        )  # Send end-of-input «None» to trigger on_finish()
        return 0, None  # exit code, exit message

    def start(self, _segment_linker):
        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            on_start_func = getattr(action, "on_start", None)
            if on_start_func:
                if DEBUG:
                    print("on_start %s " % action.action_label)
                try:
                    action._segment_linker = _segment_linker
                    on_start_func(action.initial_config)
                    action._segment_linker = None
                except:  # NOQA: E722
                    print("Failed starting", action.action_label, file=stderr)
                    raise


class SegmentManager:
    def __init__(self):
        self._segments = {}
        self.msg = Printer()

    def start(self):
        """ Runs the start code for every segment created on this manager """
        for segment_name, segment in self._segments.items():
            segment.start(self._segment_linker)

        # We must remove all references from segments which have
        # no input sources (inactive)
        for origin_segment_name, origin_segment in self._segments.items():
            origin_action = origin_segment.action_list[0]
            segment_sources = origin_action.input_sources
            if len(segment_sources) == 0:
                if origin_segment_name == "start":
                    continue
                self.msg.warn("Segment '%s' is not referenced" % origin_segment_name)
                for target_segment_name, target_segment in self._segments.items():
                    target_action = target_segment.action_list[0]
                    if origin_action in target_action.input_sources:
                        target_action.input_sources.remove(origin_action)

    def create(self, segment_name):
        segment = PipelineSegment(segment_name)
        self._segments[segment_name] = segment
        return segment

    def activate(self, activate_arguments, start_segment_name="start"):
        return self._segments[start_segment_name].activate(activate_arguments)

    def _segment_linker(self, source, segment_name):
        """ Returns a reference name to a local segment """
        try:
            segment = self._segments[segment_name]
        except KeyError:
            print(
                "A reference was found for segment '{}' which does not exist.\n"
                "The following segment names were found:\n{}\n\n".format(
                    segment_name, list(self._segments.keys())
                ),
                file=stderr,
            )
            exit(2)

        segment.action_list[0].input_sources.append(source)
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
                action_list[i + 1].input_sources.append(action)
