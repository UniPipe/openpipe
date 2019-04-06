""" This module provides the functions used to build the platform information
that is available for actions """
import platform
from pprint import pprint
import warnings


def get_platform_info():
    """ Returns the base information from the running platform """
    platform_info = {}
    for key in dir(platform):
        if key[0] == "_":
            continue
        func = getattr(platform, key)
        if not callable(func):
            continue
        try:
            with warnings.catch_warnings():  # Ignore DeprecationWarning's
                warnings.simplefilter("ignore")
                platform_info[key] = func()
        except TypeError:
            pass  # ignore functions requiring arguments
    return platform_info


if __name__ == "__main__":
    pprint(get_platform_info())
