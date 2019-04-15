""" This module provides the segment management classes """

import threading
from os import environ
from openpipe.utils import create_action_instance
from sys import stderr
from time import time
from wasabi import Printer
from queue import Queue, Empty


DEBUG = environ.get("DEBUG")

MAX_THREADS_PER_SEGMENT = int(environ.get("MAX_THREADS_PER_SEGMENT", "10"))
QSIZE_CHECK_INTERVAL = 1  # Interval between qsize checks
QSIZE_THREAD_TRIGGER = 2  # Qsize to trigger that should trigger a new thread


class PipelineSegmentRun(threading.Thread):
    def __init__(self, controller_queue):
        threading.Thread.__init__(self, controller_queue)
        self.action_list = []
        self.control_queue = Queue()
        self.controller_queue = controller_queue

    def add(self, action_name, action_config, action_label):
        action_instance = create_action_instance(
            action_name, action_config, action_label
        )
        self.action_list.append(action_instance)

    def run(self):
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
                    action.controller_queue = self.controller_queue
                    on_start_func(action.initial_config)
                    action._segment_linker = None
                except:  # NOQA: E722
                    self.control_queue.put(("failed", action.action_label))
                    return
        self.control_queue.put(("started", i))


class PipelineSegmentControl(threading.Thread):
    def __init__(self, segment_name, thread_number):
        threading.Thread.__init__(self)
        self.segment_name = segment_name
        self.control_queue = Queue()
        self.thread_list = [PipelineSegmentRun()]
        self.action_config_list = []
        self.controller_queue = Queue()

    def run(self):
        run_thread = self.thread_list[0]
        run_thread.start(self.controller_queue)

        while True:
            status, detail = run_thread.control_queue.get()
            if status in ["started", "failed"]:
                break

        if status == "failed":
            self.start_failure_list.append((self.segment_name, detail))

    def add(self, action_name, action_config, action_label):
        self.thread_list[0].add(self, action_name, action_config, action_label)
        self.self.action_config_list.append((action_name, action_config, action_label))


class PipelineSegment(threading.Thread):
    def __init__(self, segment_name, thread_number):
        threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.input_queue_list = []
        self.control_queue = Queue()
        self.name = segment_name
        self.segment_name = segment_name
        self.action_list = []
        self.config_list = []
        self.input_sources = []
        self.lock_sources = threading.RLock()
        self.thread_count = 0
        self.lock_thread_count = thread_number
        self.base_segment_info = []

    def activate(self, activate_arguments):
        if activate_arguments is not None:
            self.add_source(self)
        new_item = self, activate_arguments, {}
        self.input_queue.put(new_item)

    def add_source(self, source):
        with self.lock_sources:
            self.input_sources.append(source)

    def run(self):

        self._segment_linker = self._segment_linker

        self.loop_on_input_data()

    def loop_on_input_data(self):

        previous_time = time()

        # Loop waiting for input
        while True:
            item = self.input_queue.get()
            source, input_item, tag = item

            if input_item is None:

                # If we are not thread 0, we simply repeat the None and terminate
                # The repeated None will be used be consumed by the remaning
                # threads on the pool that need to die
                if self.thread_number != 0:
                    print("GOT NONE KILLING ME", self, self.thread_number)
                    self.input_queue.put(item)
                    self.control_queue.put((None, self))
                    return

                if source is not None:
                    with self.lock_sources:
                        self.input_sources.remove(source)
                self.action_list[0]._on_input(
                    source, None, tag
                )  # Send end-of-input «None» to trigger on_finish()
                with self.lock_sources:
                    if len(self.input_sources) == 0:
                        print("Killing me", self)
                        self.input_queue.task_done()
                        # Put None to kill any remaning threads in the pool
                        self.input_queue.put(item)
                        self.control_queue.put((None, self))
                        return
            else:
                current_time = time()
                elapsed_time = current_time - previous_time
                #  if self.thread_number == 0:
                #  input_qsize = self.input_queue.qsize()
                #  print("QSIZE", self, input_qsize, elapsed_time)
                #  If we are thread 0 and queue is increasing, report our size
                if (
                    self.thread_number == 0 and elapsed_time > QSIZE_CHECK_INTERVAL
                ):  # Only the first thread checks and reports status
                    input_qsize = self.input_queue.qsize()
                    control_qsize = self.control_queue.qsize()
                    # Don't send new qsize until a previous one was delivered
                    if control_qsize == 0 and input_qsize > QSIZE_THREAD_TRIGGER:
                        print("REPORTING needs queue", input_qsize)
                        self.control_queue.put((input_qsize, self))
                    previous_time = current_time

                self.action_list[0]._on_input(
                    source, input_item, tag
                )  # Send current time to the firs action to activate it
            self.input_queue.task_done()


class SegmentManager:
    """ This class implements the segment manager API """

    source_lock = threading.RLock()

    def __init__(self, start_segment_name):
        self.start_segment_name = start_segment_name
        self._segments = {}
        self.msg = Printer()
        self.activate_queue = Queue()

    def start(self):

        # Runs the start code for every segment created on this manage
        for segment_name, segment in self._segments.items():
            segment.start()

        start_failure_list = []

        # Get the start control data for each segment
        for segment_name, segment in self._segments.items():
            while True:
                status, detail = segment.control_queue.get()
                if status in ["started", "failed"]:
                    break
                if status == "link":
                    self.link_to_segment(detail)
            if status == "failed":
                start_failure_list.append((segment_name, detail))

        if start_failure_list:
            # Send "stop" so that all segment threads terminate
            for segment_name, segment in self._segments.items():
                segment.control_queue.put("stop")
            for failure in start_failure_list:
                print(
                    f"Failed starting segment {segment_name}, reason: {detail}",
                    file=stderr,
                )

    def kill_dead_segments(self):
        # We must remove all references from segments which have
        # no input sources (inactive)
        for origin_segment_name, origin_segment_list in self._segments.items():
            for origin_segment in origin_segment_list:
                segment_sources = origin_segment.input_sources
                if len(segment_sources) == 0:
                    if origin_segment_name == self.start_segment_name:
                        continue
                    self.msg.warn(
                        "Segment '%s' is not referenced" % origin_segment_name
                    )
                    # Kill the thread
                    origin_segment.input_queue.put((None, None, None))

    def create(self, segment_name):
        segment = PipelineSegment(segment_name, 0)
        self._segments[segment_name] = segment
        return segment

    def activate(self, activate_arguments):
        # On activation we set the called to the start segment because
        # the first element on the activated pipeline is always delivered from
        # the start segment
        start_segment = self._segments[self.start_segment_name][0]
        start_segment.activate(activate_arguments)
        start_segment.activate(None)
        active_segments = 1
        while active_segments > 0:
            active_segments = 0
            needs_more_threads = (
                []
            )  # List of segments that need more threads because input queue size is increasing
            finished_segments = []
            for segment_name, segment_list in self._segments.items():
                pivot_segment = segment_list[0]
                try:
                    print("STATUS WAIT ")
                    segment_status = pivot_segment.control_queue.get(timeout=1)
                    print("AFTER STATUS WAIT ")
                except Empty:
                    print("EMPTY", segment_name)
                    active_segments += 1
                    continue
                status_item, status_sender = segment_status
                print("STATUS", status_item, status_sender)
                if status_item is None:
                    # Wait for all the other segments threads to complete
                    for segment in segment_list[1:]:
                        segment.control_queue.get()
                    finished_segments.append(segment_name)
                else:
                    threads_count = len(segment_list)
                    if (
                        status_item > QSIZE_THREAD_TRIGGER
                        and threads_count < MAX_THREADS_PER_SEGMENT
                    ):
                        needs_more_threads.append((segment_list[0], threads_count))
                    active_segments += 1

            # Add theads to segments that are queing work
            for segment, threads_count in needs_more_threads:
                self.add_thread(segment, threads_count)

            # Remove finished_segments
            for segment_name in finished_segments:
                print("DELETING SEGMENT", segment_name)
                del self._segments[segment_name]

            print("ACTS", active_segments)

        return 0, "OK"

    def _segment_linker(self, source, segment_name):
        """ Returns a reference name to a local segment """
        try:
            segment = self._segments[segment_name][0]
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
        for segment_name, segment_list in self._segments.items():
            for segment in segment_list:
                action_list = segment.action_list
                # Create links to next on all actions  except for the last
                for i, action in enumerate(action_list[:-1]):
                    action.next_action = action_list[i + 1]

    def add_thread(self, segment, thread_number):
        """ Create a new thread for the provided segment """
        if not segment.is_alive():
            print("DEAD", segment.name)
            return
        print("NEW THREAD", segment, thread_number)
        segment_name = segment.name
        new_segment_thread = PipelineSegment(segment_name, thread_number)
        self._segments[segment_name].append(new_segment_thread)

        # New threads use the same input queue
        new_segment_thread.input_queue = segment.input_queue

        # Replicate the actions from the existing thread
        for action_name, action_config, action_label in segment.base_segment_info:
            new_segment_thread.add(action_name, action_config, action_label)

        new_segment_thread._segment_linker = self._segment_linker
        new_segment_thread.start()
        start_status, start_msg = new_segment_thread.control_queue.get()

        if start_status != 0:
            print("Failure starting action", start_msg)
            exit(1)
