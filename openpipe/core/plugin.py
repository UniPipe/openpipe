from dinterpol import Template
from sys import stderr
from traceback import print_exc
from pprint import pformat


class PluginRuntimeCore(object):

    def __init__(self, config=None):
        self.initial_config = config
        self.config_template = Template(config)
        self.failed_count = 0
        self.init()

    def _on_input(self, item):
        try:
            if item is not None:
                self.config = self.config_template.render(item)
        except:  # NOQA: E722
            print_exc(file=stderr)
            msg = (
                    "---------- Plugin %s dynamic config resolution failed ----------" % self.plugin_label)
            print(msg, file=stderr)
            print(pformat(item), file=stderr)
            #  raise(
            self.failed_count += 1
            exit(1)
        if item is None:
            on_complete_func = getattr(self, 'on_complete', None)
            if on_complete_func:
                on_complete_func()
            self.put(item)
        else:
            try:
                self.on_input(item)
            except SystemExit:
                exit(1)
            except:  # NOQA: E722
                self._execution_error(item)
            finally:
                if self.failed_count != 0:
                    exit(1)

    def _execution_error(self, item):
        print_exc(file=stderr)
        msg = (
            "---------- Plugin %s execution failed ----------, item content:"
            % (self.plugin_label))
        print(msg, file=stderr)
        print(pformat(item), file=stderr)
        self.failed_count += 1
