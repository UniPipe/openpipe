from dinterpol import Template
from sys import stderr
from os import environ
from traceback import print_exc
from pprint import pformat

ODP_RUNTIME_DEBUG = environ.get('ODP_RUNTIME_DEBUG')


class PluginRuntimeCore(object):

    def __init__(self, config=None):
        self.initial_config = config
        self.config_template = Template(config)
        self.failed_count = 0
        self.reference_count = 1
        self.init()

    def _on_input(self, item):
        try:
            if item is not None:
                self.config = self.config_template.render(item)
        except:  # NOQA: E722
            print("ITEM:\n" + pformat(item), file=stderr)
            print_exc(file=stderr)
            msg = (
                    "---------- Plugin %s dynamic config resolution failed ----------" % self.plugin_label)
            print(msg, file=stderr)
            #  raise(
            self.failed_count += 1
            exit(1)
        if item is None:
            self.reference_count -= 1
            if self.reference_count == 0:
                on_complete_func = getattr(self, 'on_complete', None)
                if on_complete_func:
                    if ODP_RUNTIME_DEBUG:
                        print("on_complete %s " % self.plugin_label)
                    on_complete_func()
                self.put(item)
        else:
            try:
                if ODP_RUNTIME_DEBUG:
                    print("on_item %s: %s" % (self.plugin_label, item))
                self.on_input(item)
            except SystemExit:
                exit(1)
            except:  # NOQA: E722
                self._execution_error(item)
            finally:
                if self.failed_count != 0:
                    exit(1)

    def _execution_error(self, item):
        print("ITEM:\n"+pformat(item), file=stderr)
        print_exc(file=stderr)
        msg = (
            "---------- Plugin %s execution failed ----------, item content:"
            % (self.plugin_label))
        print(msg, file=stderr)
        self.failed_count += 1
