""" This module provides the pipeline management class """

import sys
from os import environ
from queue import Queue
from os.path import expanduser, normpath
from openpipe.utils.download_cache import download_and_cache
from openpipe.utils.debug import debug_print
from .segment import SegmentController
from pprint import pprint
from wasabi import Printer

DEBUG = environ.get("DEBUG")

printer = Printer()


class PipelineManager:
    def __init__(self, start_segment_name):
        self.controller_queue = Queue()
        # We need a reply queue to get the link to the "start" input segment
        self.start_input_reply_queue = Queue()
        self.segment_controller = SegmentController(self.controller_queue)
        self.start_segment_name = start_segment_name
        self.start_completed = False
        self.input_completed = False
        self.load_error = False
        self.running_segments = 0

    def create_segment(self, segment_name):
        debug_print(f"Creating segment {segment_name}")
        """ Create the controller associated with a segment """
        return self.segment_controller.create_segment(segment_name)

    def is_completed(self):
        return self.running_segments == 0

    def is_started(self):
        return (self.start_completed or self.load_error) is True

    def start(self):
        debug_print(f"Starting pipeline")
        self.segment_controller.start()
        self.segment_controller.submit_message(
            cmd="request input link",
            target_segment=self.start_segment_name,
            reply_queue=self.start_input_reply_queue,
        )
        self.run_control_loop_until(self.is_started)
        debug_print(f"Start completed")

    def run_control_loop_until(self, loop_exit_func):
        debug_print("Entered run_control_loop_until() loop")
        while not loop_exit_func():
            message = self.controller_queue.get()
            debug_print(f"Got control message", message)
            try:
                cmd = message["cmd"]
                handle_func_name = "_handle_" + (cmd.replace(" ", "_"))
            except TypeError:
                print("Got invalid message:", message)
                raise
            del message["cmd"]
            try:
                getattr(self, handle_func_name)(**message)
            except:  # NOQA: E722
                print("Error processing message:")
                pprint(message)
                raise

    def activate(self, activate_arguments):
        start_input_queue = self.start_input_reply_queue.get()
        if start_input_queue is None:
            self.segment_controller.submit_message(cmd="terminate")
            sys.exit(99)
        start_input_queue.put((activate_arguments, None))
        start_input_queue.put((None, None))
        self.run_control_loop_until(self.is_completed)
        self.segment_controller.submit_message(cmd="terminate")
        return 0, "OK"

    def load_library(self, library_path):
        auto_download = environ.get("OPENPIPE_AUTO_NETWORK", "False")
        if library_path.startswith("https:"):
            if auto_download != "True":
                return
            library_path = download_and_cache(library_path, auto_install=True)
            if library_path is None:  # Remote file not found
                return
        else:
            library_path = expanduser(library_path)
        if environ.get("DEBUG"):
            print("Adding library path", library_path)
        sys.path.append(normpath(library_path))

    def plan(self, pipeline_document):
        pass

    def _handle_error(self, where, msg):
        if where == "module load":
            self.load_error = True
        printer.fail(f"Error during {where}")
        print(msg, file=sys.stderr)

    def _handle_started(self, segment_name, thread_number):
        if DEBUG:
            printer.good(f"Segment {segment_name} was started")
        if segment_name == self.start_segment_name:
            self.start_completed = True
        self.running_segments += 1

    def _handle_completed(self, segment_name):
        if DEBUG:
            printer.good(f"Segment {segment_name} input processing completed")

    def _handle_finished(self, segment_name):
        if DEBUG:
            printer.good(f"Segment {segment_name} finished")
        self.running_segments -= 1

    def _handle_debug(self, msg):
        print(msg)
