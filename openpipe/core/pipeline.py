import sys
from os import environ
from os.path import normpath, expanduser
#from .document import PipelineDocument
from .loader import FilesystemLoader
from .download_cache import download_and_cache


class PipelineRuntimeCore:

    def __init__(self, start_segment='start'):
        """
        :param filename:            The name of the file with the pipeline YAML
        :param data:                The YAML content as a string
        :param add_step_call_cb:    Callback function to be invoked when a sep is found
        """
        self.segments = {}
        self.local_only = local_only
        self.filename = filename
        self._start_segment = start_segment

    def load(self):
        self.dpl_doc.load()

    def load_plugin(self, name, params, line_nr):
        return self.plugin_loader.load(self.filename, name, params, line_nr)

    def load_libraries_cb(self, libraries):
        for libpath in libraries:
            if libpath.startswith('http:') or libpath.startswith('https:'):
                if self.local_only:  # Running in local mode, don't load external libraries
                    continue
                libpath = download_and_cache(libpath)
                if libpath is None:  # Remote file not found
                    continue
            else:
                libpath = expanduser(libpath)
            if environ.get('ODP_LIBS_DEBUG'):
                print("Adding library path", libpath)
            sys.path.append(normpath(libpath))

    @property
    def start_segment(self):
        return self.segments[self._start_segment]
