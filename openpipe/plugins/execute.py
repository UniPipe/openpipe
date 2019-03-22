"""
Execute a command and produce the execution result
"""
from openpipe.pipeline.engine import PluginRuntime
from subprocess import Popen, PIPE, STDOUT


class Plugin(PluginRuntime):

    required_config = """
    cmd:    # The command to be executed
    """
    optional_config = """
    shell:  True    # Execute the command as parameters to a system shell
    """

    def on_input(self, item):
        new_item = {}
        cmd = self.config['cmd']
        shell = self.config['shell']
        process = Popen(cmd, shell=shell, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        stdout, stderr = process.communicate()
        new_item = {
            "stdout": stdout,
            "stderr": stderr,
            "return_code": process.returncode
        }
        self.put(new_item)
