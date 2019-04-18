""" This module provides the pipeline management class """

import sys
from os import environ
from os.path import expanduser, normpath
from openpipe.utils.download_cache import download_and_cache
from .segment import SegmentController


class PipelineManager(object):
    def __init__(self, start_segment_name):
        self.controllers = {}
        self.start_segment_name = start_segment_name
        self.started_controllers = []

    def create_segment(self, segment_name):
        controller = SegmentController(segment_name)
        self.controllers[segment_name] = controller
        return controller

    def start_segment(self, controller: SegmentController):
        print("\nSTARTING SEGMENT", controller.name)
        controller.start()
        while True:
            print("Waiting for input request")
            need_request = controller.get()
            print(", needed_input")
            if need_request is None:
                break
            needed_input, reply_queue = need_request
            needed_controller = self.controllers[needed_input]
            if needed_controller in self.started_controllers:
                needed_controller.provide_input_for(reply_queue)
                self.started_controllers.append(needed_controller)
            else:
                self.start_segment(needed_controller)
        controller.put(None)

    def start(self):
        """
        """
        start_controller = self.controllers[self.start_segment_name]
        self.start_segment(start_controller)

    def activate(self, activate_arguments):
        return self.segment_manager.activate(activate_arguments)

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
