""" This module provides the pipeline management class """

import sys
from os import environ
from os.path import expanduser, normpath
from openpipe.utils.download_cache import download_and_cache
from .segment import SegmentManager


class PipelineManager:
    def __init__(self):
        self.segment_manager = SegmentManager()

    def create_segment(self, segment_name):
        return self.segment_manager.create(segment_name)

    def start(self):
        self.segment_manager.start()

    def activate(self, activate_arguments):
        return self.segment_manager.activate(activate_arguments)

    def create_action_links(self):
        """ Create all links required to exchange data between action instances """
        self.segment_manager.create_action_links()

    def load_library(self, library_path):
        if library_path.startswith("http:") or library_path.startswith("https:"):
            library_path = download_and_cache(library_path)
            if library_path is None:  # Remote file not found
                return
        else:
            library_path = expanduser(library_path)
        if environ.get("DEBUG"):
            print("Adding library path", library_path)
        sys.path.append(normpath(library_path))
