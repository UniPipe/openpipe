""" This module provides the action runtime classes """

from dinterpol import Template
from sys import stderr
from os import environ, sep
from traceback import print_exc
from pprint import pformat
from os.path import join, dirname
from importlib import import_module
from glob import glob

DEBUG = environ.get("DEBUG")


class ActionRuntimeBase:
    def __init__(self, action_config, action_label):
        self.initial_config = action_config
        self.action_label = action_label
        self._tag = None
        self.config_template = Template(action_config)
        self.failed_count = 0
        self.init()

    def segment_linker(self, segment_name):
        return self._segment_linker(self, segment_name)

    def _on_input(self, caller, item, tag_item):
        _debug = isinstance(tag_item, dict) and tag_item.get("_debug", False)
        if DEBUG or _debug:
            print(
                "on_input %s: \n\tInput: %s\n\tTag: %s"
                % (self.action_label, item, tag_item)
            )
        if item is not None:
            self._tag = tag_item
            try:
                self.config = self.config_template.render(item, tag_item)
            except:  # NOQA: E722
                if isinstance(item, bytes) and len(item) > 256:
                    item = item[:255]
                print("ITEM:\n" + pformat(item), file=stderr)
                if tag_item:
                    print("TAG ITEM:\n" + pformat(tag_item), file=stderr)
                print_exc(file=stderr)
                msg = (
                    "---------- Action %s dynamic config resolution failed ----------"
                    % self.action_label
                )
                print(msg, file=stderr)
                #  raise(
                self.failed_count += 1
                exit(1)

        if item is None:
            on_finish_func = getattr(self, "on_finish", None)
            if on_finish_func:
                if DEBUG or _debug:
                    print("on_finish %s [Tag: %s]" % (self.action_label, self._tag))
                on_finish_func(True)
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
        if isinstance(item, bytes) and len(item) > 256:
            item = item[:255]
        print("ITEM:\n" + pformat(item), file=stderr)
        if self._tag:
            print("TAG ITEM:\n" + pformat(self._tag), file=stderr)
        print_exc(file=stderr)
        msg = "---------- Action %s execution failed ----------, item content:" % (
            self.action_label
        )
        print(msg, file=stderr)
        self.failed_count += 1

    def extend(self, action_path, extension_path):
        """ Extend action by importing modules from extension path """
        location = join(dirname(action_path), extension_path)
        sub_modules = glob(join(location, "*.py"))
        for filename in sub_modules:
            filename = ".".join(filename.split(sep)[-6:])
            filename = filename.rsplit(".", 1)[0]
            import_module(filename)


class ActionRuntime(ActionRuntimeBase):
    def init(self):
        self.next_action = None

    def put(self, item):

        # Put on next
        if self.next_action:
            self.next_action._on_input(self, item, self._tag)

    def put_target(self, item, target):
        target.put((self, item, self._tag))

    def set_tag(self, tag_item):
        if DEBUG:
            print("set_tag %s : " % self.action_label, tag_item)
        self._tag = tag_item
