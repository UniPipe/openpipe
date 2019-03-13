from openpipe.engine import PluginRuntime
from openpipe.core.config_validation import validate_config


def test_missing_required_some_config():

    class Plugin(PluginRuntime):
        required_some_config = """ YES """
    try:
        validate_config(Plugin, "", None)
    except SystemExit as ex:
        assert(ex.code == 25)
    else:
        raise


def test_required_some_config():

    class Plugin(PluginRuntime):
        required_some_config = """ YES """

    result = validate_config(Plugin, "", "plain")
    assert(result == "plain")


def test_zero_config():

    class Plugin(PluginRuntime):
        pass

    validate_config(Plugin, "", None)
    try:
        validate_config(Plugin, "", "Something")
    except SystemExit as ex:
        assert(ex.code == 20)
    else:
        raise


def test_required_is_not_dict():

    class Plugin(PluginRuntime):
        required_config = ""
    try:
        validate_config(Plugin, "", None)
    except AssertionError:
        pass
    else:
        raise


def test_required_contains_default():

    class Plugin(PluginRuntime):
        required_config = """
        key1: 12
        """
    try:
        validate_config(Plugin, "", None)
    except AssertionError:
        pass
    else:
        raise


def test_required_multi_dict_with_non_dict_config():

    class Plugin(PluginRuntime):
        required_config = """
        key1:
        key2:
        """
    try:
        validate_config(Plugin, "", "someone")
    except SystemExit as ex:
        assert(ex.code == 21)
    else:
        raise


def test_required_single_dict_with_non_dict_config():

    class Plugin(PluginRuntime):
        required_config = """
        key1:
        """
    result = validate_config(Plugin, "", "someone")
    assert(result == {"key1": "someone"})


def test_required_single_dict_with_missing_config():

    class Plugin(PluginRuntime):
        required_config = """
        key1:
        """
    try:
        validate_config(Plugin, "", {"some": "value"})
    except SystemExit as ex:
        assert(ex.code == 22)
    else:
        raise


def test_optional_non_dict_with_required_config():

    class Plugin(PluginRuntime):
        required_config = """
        key1:
        """
        optional_config = "some"
    try:
        validate_config(Plugin, "", "ok")
    except AssertionError:
        pass
    else:
        raise


def test_optional_non_dict_with_non_dict_provided():

    class Plugin(PluginRuntime):
        optional_config = "some"

    result = validate_config(Plugin, "", None)
    assert(result == "some")
    result = validate_config(Plugin, "", "from_user")
    assert(result == "from_user")
    result = validate_config(Plugin, "", ["ok"])
    assert(result == ["ok"])


def test_optional_non_dict_with_dict_provided():

    class Plugin(PluginRuntime):
        optional_config = "some"

    result = validate_config(Plugin, "", {"just": "one"})
    assert(result == {"just": "one"})


def test_optional_dict_with_non_dict_provided():

    class Plugin(PluginRuntime):
        optional_config = """
        key1: simple
        """
    try:
        validate_config(Plugin, "", "ahaha")
    except SystemExit as ex:
        assert(ex.code == 23)
    else:
        raise


def test_optional_dict_with_non_supported():

    class Plugin(PluginRuntime):
        optional_config = """
        key1: simple
        """
    try:
        validate_config(Plugin, "", {"key2": 12})
    except SystemExit as ex:
        assert(ex.code == 24)
    else:
        raise


def test_optional_dict_with_user_valid():

    class Plugin(PluginRuntime):
        optional_config = """
        key1: simple
        """
    result = validate_config(Plugin, "", None)
    assert(result == {"key1": "simple"})
    result = validate_config(Plugin, "", {"key1": "better"})
    assert(result == {"key1": "better"})


def test_optional_dict_with_user_valid_part():

    class Plugin(PluginRuntime):
        optional_config = """
        key1: simple
        key2: more
        """
    result = validate_config(Plugin, "", None)
    assert(result == {"key1": "simple", "key2": "more"})
    result = validate_config(Plugin, "", {"key1": "better"})
    assert(result == {"key1": "better", "key2": "more"})
