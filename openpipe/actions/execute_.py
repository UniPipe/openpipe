"""
Execute a command and produce the execution result
"""
from openpipe.pipeline.engine import ActionRuntime
from subprocess import Popen, PIPE


class Action(ActionRuntime):

    category = "Data Sourcing"

    required_config = """
    cmd:    # The command to be executed
    """
    optional_config = """
    shell:  True    # Execute the command as parameters to a system shell
    output_as_text: True # Output the command output as text
    fail_on_error: True  # Abort pipeline if exit code is not zero
    """

    def on_input(self, item):
        new_item = {}
        cmd = self.config["cmd"]
        shell = self.config["shell"]
        process = Popen(
            cmd, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True
        )
        stdout, stderr = process.communicate()
        if self.config["output_as_text"]:
            if stdout:
                stdout = stdout.decode("utf-8")
            if stderr:
                stderr = stderr.decode("utf-8")
        if process.returncode != 0 and self.config["fail_on_error"]:
            raise Exception(stderr)
        new_item = {
            "stdout": stdout,
            "stderr": stderr,
            "return_code": process.returncode,
        }
        self.put(new_item)
