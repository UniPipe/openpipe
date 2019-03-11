from openpipe.cli.run import run_test
from os.path import join


def test_libraries():
    exit_code, exit_message = run_test(join('openpipe', 'tests', 'libraries.yaml'))
    print(exit_code, exit_message)
    if exit_code != 0:
        raise Exception(exit_message)
