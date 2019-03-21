import sys
import click
from .run import run
from .help import help
from . import version
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
@click.version_option(version=version)
def cli():
    pass


cli.add_command(run)
cli.add_command(help)


def main():
    cli()


if __name__ == "__main__":
    main()
