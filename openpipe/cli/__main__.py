import sys
import click
from .show import cmd_show
from .run import cmd_run
from .help import cmd_help
from .test import cmd_test
from .actionmanager import cmd_install_action_lib, cmd_list_action_lib
from ..about import __version__
from os import environ
import colorama

# ANSI chars conversion for Windows
colorama.init()


def tracefunc(frame, event, arg, indent=[0]):
    if event == "call":
        indent[0] += 2
        print("-" * indent[0] + "> call function", frame.f_code.co_name)
    elif event == "return":
        print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        indent[0] -= 2
    return tracefunc


if environ.get("TRACE"):
    sys.settrace(tracefunc)


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(cmd_help)
cli.add_command(cmd_run)
cli.add_command(cmd_show)
cli.add_command(cmd_test)
cli.add_command(cmd_install_action_lib)
cli.add_command(cmd_list_action_lib)


def main():
    cli()


if __name__ == "__main__":
    main()
