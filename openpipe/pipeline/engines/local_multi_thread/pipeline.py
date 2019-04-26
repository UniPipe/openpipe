""" This module provides the pipeline management class """

import sys
from queue import Queue
from os import environ
from os.path import expanduser, normpath
from openpipe.utils.download_cache import download_and_cache
from .segment import SegmentController


class PipelineManager(object):
    def __init__(self, start_segment_name):
        self.controllers = {}
        self.start_segment_name = start_segment_name
        self.started_controllers = []
        self.activate_queue = None

    def create_segment(self, segment_name):
        """ Create the controller associated with a segment """
        controller = SegmentController(segment_name)
        self.controllers[segment_name] = controller
        return controller

    def start_segment(self, controller: SegmentController):
        """
        Start a segment controller.
        If this segment requires additional segments which have not been loaded,
        start then first.
        """
        controller.start()
        # Loop until the segment and any dependent segment controllers
        # are started
        while True:
            # First wait for the list of  needed segments
            if controller.name == "Controller_do_something":
                print("Waiting for the list of needed segments", controller.name)
            start_reply = controller.get()
            if controller.name == "Controller_do_something":
                print("Got list of needed segments", start_reply)
            status, title, detail = start_reply
            if status == "failed":
                print("Startup failed")
                print(detail)
                print(title)
                exit(1)
            elif status == "request input":
                segment_name, reply_queue = title, detail
                return self.handle_request_input(segment_name, reply_queue)
            elif status == "started":
                break
            else:
                raise NotImplementedError(status)
        controller.put("running")

    def handle_request_input(self, segment_name, reply_queue):
        """ Answer to an input request """
        print("handle_request_input", segment_name)
        # This segment requires additional segments
        needed_controller = self.controllers[segment_name]
        if needed_controller in self.started_controllers:
            needed_controller.provide_input_to(reply_queue)
        else:
            print("Starting new controller for", segment_name)
            self.started_controllers.append(needed_controller)
            self.start_segment(needed_controller)
            needed_controller.provide_input_to(reply_queue)
        print("Done - handle_request_input", segment_name)

    def start(self):
        """
        """
        start_controller = self.controllers[self.start_segment_name]
        self.start_segment(start_controller)
        reply_queue = Queue()
        # start_controller.put("request input", self.start_segment_name, reply_queue)
        # reply = reply_queue.get()
        start_controller.provide_input_to(reply_queue)
        self.activate_queue = reply_queue.get()

    def activate(self, activate_arguments):
        self.activate_queue.put(activate_arguments)
        print("Activation completed")

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
