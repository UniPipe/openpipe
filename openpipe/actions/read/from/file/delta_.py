"""
Produce text file changes between consecutive executions
"""


from os import stat
from os.path import exists
from openpipe.pipeline.engine import ActionRuntime


class Action(ActionRuntime):

    optional_config = """
    path: $_$               # Path to the file to be read
    headers_always: False   # Always send header lines of file
    state_file: ""          # If set it will be used save state between executions
    """

    def on_start(self, config):
        self._state = {}
        self.first_run = True
        if config["headers_always"]:
            self.on_input = self.on_first
        else:
            self.on_input = self.on_input_delta

    def on_first(self, item):

        path = self.config["path"]
        # On the first run, if "headers_always", we read and produce the headers
        with open(path) as data_file:
            for line in data_file:
                line = str(line).strip("\r\n")
                if line and line[0] == "#":
                    self.put(line)
                else:
                    break

        self.on_input = self.on_input_delta
        self.on_input(item)

    def on_input_delta(self, item):  # NOQA: C901
        path = self.config["path"]

        # Get saved info from last execution
        saved_mod_time, saved_last_size = self._get_last_run_info(path)

        # Get current file info
        statbuf = stat(path)
        current_mod_time, current_size = int(statbuf.st_mtime), statbuf.st_size

        # If no saved info was found, save current info, and do nothing
        if saved_mod_time is None:
            self._set_last_run_info(path, current_mod_time, current_size)
            return

        file_was_changed = (
            current_mod_time != saved_mod_time or current_size != saved_last_size
        )

        # If there are no changes, do nothing
        if not file_was_changed:
            return

        #  If it was truncated, start from begin of file
        if current_size < saved_last_size:
            saved_last_size = 0
        line_prefix = None

        with open(path) as data_file:

            # Start from last position
            if saved_last_size:
                self._seek_position(data_file, saved_last_size)

            line = data_file.readline()
            while line:
                # Refresh the current size after the the data is read
                line = str(line).strip("\r\n")
                if line_prefix:
                    line = line_prefix + " " + line
                self.put(line)
                line = data_file.readline()
            current_size = data_file.tell()
        self._set_last_run_info(path, current_mod_time, current_size)

    def _seek_position(self, file, position):
        """
        Check if there are any changes to the file since last run
        @return: True if changes are found, False if not
        """
        file.seek(0, 2)  # go to end of file
        file.seek(position)

    def _set_last_run_info(self, path, mod_time, size):
        self._state[path] = mod_time, size

        if self.config["state_file"]:
            with open(self.config["state_file"], "w") as file:
                file.write(f"{mod_time}:{size}\n")

    def _get_last_run_info(self, path):
        state_filename = self.config["state_file"]
        if state_filename and exists(state_filename):
            with open(state_filename, "r") as file:
                line = file.read()
            if ":" in line:
                mtime, msize = line.split(":")
                return int(mtime), int(msize)
        mod_time, size = self._state.get(path, (None, None))
        return mod_time, size
