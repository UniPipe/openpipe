from os import environ

DEBUG = environ.get("DEBUG")


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
