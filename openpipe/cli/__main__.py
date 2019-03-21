from .run import run
from .help import help
from . import version
import click


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
