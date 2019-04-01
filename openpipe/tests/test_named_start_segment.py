from openpipe.cli.run import pipeline_run


def test_default_start():
    exit_code, exit_message = pipeline_run(
        "openpipe/tests/test_named_start_segment.yaml", start_segment="good segment"
    )
    print(exit_code, exit_message)
    if exit_code != 0:
        raise Exception(exit_message)
