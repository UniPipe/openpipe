from .cli.run import run
from .cli.help import help
from .cli import version
import click


@click.group()
@click.version_option(version=version)
def cli():
    pass


cli.add_command(run)
cli.add_command(help)


def main():
    cli()


if __name__ == '__main__':
    main()
