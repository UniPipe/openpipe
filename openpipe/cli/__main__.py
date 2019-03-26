import sys
import click
from .run import cmd_run
from .help import cmd_help
from .test import cmd_test
from .pluginmanager import install_plugin
from ..about import __version__
from os import environ


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


cli.add_command(cmd_run)
cli.add_command(cmd_help)
cli.add_command(cmd_test)
cli.add_command(install_plugin)


def main():
    cli()


if __name__ == "__main__":
    main()
