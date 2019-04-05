""" This module provides the functions used to build the platform information
that is available for actions """

import platform


def get_info():
    """ Returns the base information from the running platform """
    platform_info = {}
    for key in dir(platform):
        if key[0] == "_":
            continue
        if key in ['popen', 'system_alias', 'uname_result']:
            continue
        func = getattr(platform, key)
        if not callable(func):
            continue
        platform_info[key] = func()
    return platform_info
