from openpipe.cli.run import pipeline_run


def test_libraries():
    exit_code, exit_message = pipeline_run(
        "openpipe/tests/libraries.yaml", ()
    )
    print(exit_code, exit_message)
    if exit_code != 0:
        raise Exception(exit_message)
