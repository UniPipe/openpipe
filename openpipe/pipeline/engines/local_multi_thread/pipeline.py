""" This module provides the pipeline management class """

import sys
from os import environ
from os.path import expanduser, normpath
from openpipe.utils.download_cache import download_and_cache
from .segment import SegmentManager


class PipelineManager:
    def __init__(self, start_segment_name):
        self.segment_managers = {}
        self.start_segment_name = start_segment_name

    def create_segment(self, segment_name):
        segment_manager = SegmentManager(segment_name)
        self.segment_managers[segment_name] = segment_manager
        return self.segment_manager.create(segment_name)

    def start(self):
        started_segments = []
        pending_link_requests = []
        start_segment_manager = self.segment_managers[self.start_segment_name]
        start_segment_manager.control_in.put("GET LINK")
        pending_link_requests.append(self, start_segment_manager)

        while True:
            resolved_requests = []
            for requester, requested_segment_manager in pending_link_requests:
                status, argument = requested_segment_manager.control_out.get()
                if status == "GET LINK":
                    new_requested_segment_manager = self.segment_managers[argument]
                    pending_link_requests.append(
                        requested_segment_manager, new_requested_segment_manager
                    )
                elif status == "USE LINK":
                    if requester == self:  # Got link for the start segment
                        break
                    if requested_segment_manager not in started_segments:
                        started_segments.append(requested_segment_manager)
                    requester.control_in.send("USE LINK", argument)
                    resolved_requests.append(requester, requested_segment_manager)
                elif status == "ERROR":
                    print(
                        "ERROR starting segment",
                        requested_segment_manager,
                        file=sys.stderr,
                    )
                    exit(2)

            for delete_request in resolved_requests:
                pending_link_requests.remove(delete_request)

        for segment_manager in started_segments:
            segment_manager.send("ACTIVATE", None)

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
        config = pipeline_document.get("_local_multi_thread", None)
        if config:
            self.thread_pools_config = config.get("thread_pools", {})

        print("CFG PLAN IS", self.thread_pools_config)
