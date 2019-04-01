from os import environ
from openpipe.cli.run import pipeline_run


def test_local_lib():
    exit_code, exit_message = pipeline_run("openpipe/tests/libraries.yaml")
    print(exit_code, exit_message)
    if exit_code != 0:
        raise Exception(exit_message)


def test_remote_lib():
    try:
        exit_code, exit_message = pipeline_run("openpipe/tests/libraries_auto_net.yaml")
    except ModuleNotFoundError:
        pass
    else:
        raise Exception("Loaded file without net enabled")
    environ["OPENPIPE_AUTO_NETWORK"] = "True"
    exit_code, exit_message = pipeline_run("openpipe/tests/libraries_auto_net.yaml")
    print(exit_code, exit_message)
    if exit_code != 0:
        raise Exception(exit_message)
