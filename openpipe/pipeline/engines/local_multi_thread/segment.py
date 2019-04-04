""" This module provides the segment management classes """

from os import environ
from openpipe.utils import create_action_instance
from sys import stderr
import threading
from wasabi import Printer
from queue import Queue

DEBUG = environ.get("DEBUG")


class PipelineSegment(threading.Thread):
    def __init__(self, segment_name, thread_number=0):
        threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.input_queue_list = []
        self.input_queue = Queue()
        self.control_queue = Queue()
        self.name = segment_name
        self.segment_name = segment_name
        self.action_list = []
        self.config_list = []
        self.input_sources = []
        self.lock_sources = threading.RLock()
        self.thread_count = 0
        self.lock_thread_count = thread_number

    def add(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label
        )
        self.action_list.append(action_instance)
        self.config_list.append(action_config)

    def activate(self, activate_arguments):
        if activate_arguments is not None:
            self.add_source(self)
        new_item = self, activate_arguments, {}
        self.input_queue.put(new_item)

    def add_source(self, source):
        with self.lock_sources:
            self.input_sources.append(source)

    def run(self):

        _segment_linker = self._segment_linker

        """ Run the on start method for all the actions in this segment """
        for i, action in enumerate(self.action_list):
            action.action_label = (
                "Thread-'" + self.segment_name + "' :" + action.action_label
            )
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
                    self.control_queue.put((-1, action.action_label))
                    return
        self.control_queue.put((0, "OK " + self.segment_name))

        # Loop waiting for input
        while True:
            item = self.input_queue.get()
            source, input_item, tag = item
            if input_item is None:
                if source is not None:
                    with self.lock_sources:
                        self.input_sources.remove(source)
                self.action_list[0]._on_input(
                    source, None, tag
                )  # Send end-of-input «None» to trigger on_finish()
                with self.lock_sources:
                    if len(self.input_sources) == 0:
                        self.input_queue.task_done()
                        return
            else:
                self.action_list[0]._on_input(
                    source, input_item, tag
                )  # Send current time to the firs action to activate it
            self.input_queue.task_done()


class SegmentManager:

    source_lock = threading.RLock()

    def __init__(self, start_segment_name):
        self.start_segment_name = start_segment_name
        self._segments = {}
        self.msg = Printer()
        self.activate_queue = Queue()

    def start(self):

        """ Runs the start code for every segment created on this manager """
        for segment_name, segment in self._segments.items():
            segment._segment_linker = self._segment_linker
            segment.start()

        for segment_name, segment in self._segments.items():
            start_status, start_msg = segment.control_queue.get()
            if start_status != 0:
                print("Failure starting action", start_msg)
                exit(1)

        self.kill_dead_segments()

    def kill_dead_segments(self):
        # We must remove all references from segments which have
        # no input sources (inactive)
        for origin_segment_name, origin_segment in self._segments.items():
            segment_sources = origin_segment.input_sources
            if len(segment_sources) == 0:
                if origin_segment_name == self.start_segment_name:
                    continue
                self.msg.warn("Segment '%s' is not referenced" % origin_segment_name)
                # Kill the thread
                origin_segment.input_queue.put((None, None, None))

    def create(self, segment_name):
        segment = PipelineSegment(segment_name)
        self._segments[segment_name] = segment
        return segment

    def activate(self, activate_arguments):
        # On activation we set the called to the start segment because
        # the first element on the activated pipeline is always delivered from
        # the start segment
        start_segment = self._segments[self.start_segment_name]
        start_segment.activate(activate_arguments)
        start_segment.activate(None)
        for segment in self._segments.values():
            segment.join()
        return 0, "OK"

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
        segment.add_source(source)
        return segment.input_queue

    def create_action_links(self):
        """ Create links between consecutive action and on segment references
        In a simple single threaded pipeline, the link is just a memory reference """

        # Links for consecutive steps for each segment
        for segment_name, segment in self._segments.items():
            action_list = segment.action_list
            # Create links to next on all actions  except for the last
            for i, action in enumerate(action_list[:-1]):
                action.next_action = action_list[i + 1]
