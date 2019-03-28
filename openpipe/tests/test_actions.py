from openpipe.cli.run import pipeline_run
from os.path import join
import os


def collect_test_files():
    test_files = []
    for root, dirs, files in os.walk(join("openpipe", "actions")):
        for file in files:
            if file.endswith("_test.yaml"):
                test_files.append(os.path.join(root, file))
    return test_files


test_file = os.environ.get("TEST_FILE")
if test_file:
    test_files_list = [test_file]
else:
    test_files_list = collect_test_files()


def pytest_generate_tests(metafunc):
    id_list = []
    argvalues = []
    #  os_system = platform.system()
    for test_file in metafunc.cls.test_files:
        id_list.append(test_file)
        argnames = ["test_filename"]
        argvalues.append(([test_file]))
        # if os_system != 'Windows' and 'command' in test_file:
        #    argnames.append("conf")
        #    argvalues.append(([pytest.skip("Smoke tests must....")]))

    metafunc.parametrize(argnames, argvalues, ids=id_list, scope="class")


# if os_system != 'Windows' and test_file in WIN_ONLY:
#     argnames.append("conf")
#     argvalues.append(pytest.skip("Smoke tests must...."))


class TestPipeline(object):
    test_files = test_files_list

    def test(self, test_filename):
        exit_code, exit_message = pipeline_run(test_filename)
        print(exit_code, exit_message)
        if exit_code != 0:
            raise Exception(exit_message)
