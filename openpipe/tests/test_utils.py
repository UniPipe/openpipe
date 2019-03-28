""" Some testes for the utils functions """
from openpipe.utils import get_actions_metadata
from pprint import pprint


def test_actions_metadata():
    actions_meta_data = get_actions_metadata()
    pprint(actions_meta_data)
