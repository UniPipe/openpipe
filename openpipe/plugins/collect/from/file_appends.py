"""
Insert text file line appends between consecutive executions
"""

from glob import glob
from os import stat
from os.path import expanduser
from datetime import datetime
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):

    optional_config = """
    path: $_$                   # Name of file to be checked for changes
    mark_line: ""               # If set, send this line on every run
                                # usefull to distinguish groups between iterations
    persistent_state: False     # Store the last file position in an sqlite db
    prefix_path: False          # Prefix lines with the file name
    prefix_timestamp: False     # Prefix lines with timestamp
    max_delta_time: 0           # Don't send lines whentime delta > max delta time
    head_comments: False        # On first run allways send heading comments
                                # used for ms_iis_logs parsing, to get header field names
    """

    def on_start(self, config, segment_resolver):
        self._state = {}
        self.first_run = True
        self.on_input_delta = self.on_input
        if config["head_comments"]:
            self.on_input = self.on_input_head

    def on_input_head(self, item):
        path = self._get_path(item)
        # On the first run, if "head_comments", we read and produce the headers
        with open(path) as data_file:
            for line in data_file:
                line = str(line).strip('\r\n')
                if line and line[0] == "#":
                    self.put(line)
                else:
                    break
        self.on_input = self.on_input_delta
        self.on_input(item)

    def on_input(self, item):   # NOQA: C901
        path = self._get_path(item)

        # Get saved info from last execution
        saved_mod_time, saved_last_size = self._get_last_run_info(path)

        # Get current file info
        statbuf = stat(path)
        current_mod_time, current_size = int(statbuf.st_mtime), statbuf.st_size

        max_delta_time = self.config['max_delta_time']
        if max_delta_time and saved_mod_time and current_mod_time - saved_mod_time > max_delta_time:
            # If modified time is too old, ignore saved time
            saved_mod_time = None

        # If no saved info was found, save current info, and do nothing
        if saved_mod_time is None:
            self._set_last_run_info(path, current_mod_time, current_size)
            return

        if self.config['mark_line']:
            self.put(path + " " + self.config['mark_line'])

        file_was_changed = (current_mod_time != saved_mod_time or current_size != saved_last_size)

        # If there are no changes, do nothing
        if not file_was_changed:
            return

        #  If it was truncated, start from begin of file
        if current_size < saved_last_size:
            saved_last_size = 0
        line_prefix = None

        if self.config['prefix_timestamp']:
            line_prefix = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(path) as data_file:

            # Start from last position
            if saved_last_size:
                self._seek_position(data_file, saved_last_size)

            line = data_file.readline()
            while line:
                # Refresh the current size after the the data is read
                line = str(line).strip('\r\n')
                # Skip to saved_last_size when "collecting_headers" and a non comment line was found
                if self.config["prefix_path"]:
                    line = path + " " + line
                if line_prefix:
                    line = line_prefix + " " + line
                self.put(line)
                line = data_file.readline()
            current_size = data_file.tell()
        self._set_last_run_info(path, current_mod_time, current_size)

    def _get_path(self, item):
        item_path = self.config['path']
        path = expanduser(item_path)
        if '*' in path:
            path = glob(path)
            if not path:
                raise Exception("No file found at "+path)
            path = path[-1]
        return path

    def _seek_position(self, file, position):
        """
        Check if there are any changes to the file since last run
        @return: True if changes are found, False if not
        """
        file.seek(0, 2)                         # go to end of file
        file.seek(position)

    def _set_last_run_info(self, path, mod_time, size):
        if not self.config['persistent_state']:
            self._state[path] = mod_time, size
            return

        self.cursor.execute(
            "INSERT OR IGNORE INTO last_run_info VALUES('{0}', {1}, {2})"
            .format(path, mod_time, size)
        )
        self.cursor.execute(
            "UPDATE last_run_info SET modified={1}, size={2} WHERE path='{0}'"
            .format(path, mod_time, size)
        )
        self.conn.commit()

    def _get_last_run_info(self, path):
        if not self.config['persistent_state']:
            mod_time, size = self._state.get(path, (None, None))
            return mod_time, size
        self.cursor.execute("SELECT modified, size FROM last_run_info WHERE path = '%s'" % path)
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None, None
