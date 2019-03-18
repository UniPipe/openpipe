from openpipe.engine import PluginRuntime
from openpipe.core.params_validation import validate_params


def test_missing_required_some_params():

    class Plugin(PluginRuntime):
        required_some_params = """ YES """
    try:
        validate_params(Plugin, "", None)
    except SystemExit as ex:
        assert(ex.code == 25)
    else:
        raise


def test_required_some_params():

    class Plugin(PluginRuntime):
        required_some_params = """ YES """

    result = validate_params(Plugin, "", "plain")
    assert(result == "plain")


def test_zero_params():

    class Plugin(PluginRuntime):
        pass

    validate_params(Plugin, "", None)
    try:
        validate_params(Plugin, "", "Something")
    except SystemExit as ex:
        assert(ex.code == 20)
    else:
        raise


def test_required_is_not_dict():

    class Plugin(PluginRuntime):
        required_params = ""
    try:
        validate_params(Plugin, "", None)
    except AssertionError:
        pass
    else:
        raise


def test_required_contains_default():

    class Plugin(PluginRuntime):
        required_params = """
        key1: 12
        """
    try:
        validate_params(Plugin, "", None)
    except AssertionError:
        pass
    else:
        raise


def test_required_multi_dict_with_non_dict_params():

    class Plugin(PluginRuntime):
        required_params = """
        key1:
        key2:
        """
    try:
        validate_params(Plugin, "", "someone")
    except SystemExit as ex:
        assert(ex.code == 21)
    else:
        raise


def test_required_single_dict_with_non_dict_params():

    class Plugin(PluginRuntime):
        required_params = """
        key1:
        """
    result = validate_params(Plugin, "", "someone")
    assert(result == {"key1": "someone"})


def test_required_single_dict_with_missing_params():

    class Plugin(PluginRuntime):
        required_params = """
        key1:
        """
    try:
        validate_params(Plugin, "", {"some": "value"})
    except SystemExit as ex:
        assert(ex.code == 22)
    else:
        raise


def test_optional_non_dict_with_requiredl_params():

    class Plugin(PluginRuntime):
        required_params = """
        key1:
        """
        optional_params = "some"
    try:
        validate_params(Plugin, "", "ok")
    except AssertionError:
        pass
    else:
        raise


def test_optional_non_dict_with_non_dict_provided():

    class Plugin(PluginRuntime):
        optional_params = "some"

    result = validate_params(Plugin, "", None)
    assert(result == "some")
    result = validate_params(Plugin, "", "from_user")
    assert(result == "from_user")
    result = validate_params(Plugin, "", ["ok"])
    assert(result == ["ok"])


def test_optional_non_dict_with_dict_provided():

    class Plugin(PluginRuntime):
        optional_params = "some"

    result = validate_params(Plugin, "", {"just": "one"})
    assert(result == {"just": "one"})


def test_optional_dict_with_non_dict_provided():

    class Plugin(PluginRuntime):
        optional_params = """
        key1: simple
        """
    try:
        validate_params(Plugin, "", "ahaha")
    except SystemExit as ex:
        assert(ex.code == 23)
    else:
        raise


def test_optional_dict_with_non_supported():

    class Plugin(PluginRuntime):
        optional_params = """
        key1: simple
        """
    try:
        validate_params(Plugin, "", {"key2": 12})
    except SystemExit as ex:
        assert(ex.code == 24)
    else:
        raise


def test_optional_dict_with_user_valid():

    class Plugin(PluginRuntime):
        optional_params = """
        key1: simple
        """
    result = validate_params(Plugin, "", None)
    assert(result == {"key1": "simple"})
    result = validate_params(Plugin, "", {"key1": "better"})
    assert(result == {"key1": "better"})


def test_optional_dict_with_user_valid_part():

    class Plugin(PluginRuntime):
        optional_params = """
        key1: simple
        key2: more
        """
    result = validate_params(Plugin, "", None)
    assert(result == {"key1": "simple", "key2": "more"})
    result = validate_params(Plugin, "", {"key1": "better"})
    assert(result == {"key1": "better", "key2": "more"})
