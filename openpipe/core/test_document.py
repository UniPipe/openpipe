from .document import PipelineDocument


def test_yaml_syntax_error():
    doc = PipelineDocument(yaml_data="-\n:")
    try:
        doc.load()
    except SystemExit:
        pass
    else:
        raise


def test_invalid_step_formats():
    """ Test detection of invalid step formats """
    yaml_data = """
    start:
        not a good step:
    """

    doc = PipelineDocument(yaml_data=yaml_data)
    try:
        doc.load()
    except SystemExit:
        pass
    else:
        raise


def test_valid_steps():
    """ Test detection of valid step formats """

    yaml_data = """
    start:
        - step 1:
        - step 2:
    """
    doc = PipelineDocument(yaml_data=yaml_data)
    doc.load()
