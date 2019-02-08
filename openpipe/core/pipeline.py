import sys
from os import environ
from os.path import normpath, expanduser
from .document import PipelineDocument
from .loader import FilesystemLoader
from .download_cache import download_and_cache


class PipelineRuntimeCore(object):

    def __init__(self, filename=None, data=None):
        """
        :param filename:            The name of the file with the pipeline YAML
        :param data:                The YAML content as a string
        :param add_step_call_cb:    Callback function to be invoked when a sep is found
        """
        self.segments = {}
        self.filename = filename
        self.dpl_doc = PipelineDocument(filename, data, self.add_step_cb, self.load_libraries_cb)
        self.plugin_loader = FilesystemLoader("openpipe/plugins")

    def load(self):
        self.dpl_doc.load()

    def load_plugin(self, name, config, line_nr):
        return self.plugin_loader.load(self.filename, name, config, line_nr)

    def load_libraries_cb(self, libraries):
        for libpath in libraries:
            if libpath.startswith('http:') or libpath.startswith('https:'):
                libpath = download_and_cache(libpath)
            else:
                libpath = expanduser(libpath)
            if environ.get('MDP_LIBS_DEBUG'):
                print("Adding library path", libpath)
            sys.path.append(normpath(libpath))

    @property
    def start_segment(self):
        if len(self.segments) == 1:
            start_segment_name = next(iter(self.segments))
        else:
            start_segment_name = 'start'
        return self.segments[start_segment_name]
