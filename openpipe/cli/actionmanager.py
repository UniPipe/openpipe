import click
from ..utils.download_cache import download_and_cache


@click.command(name="install-action-lib")
@click.option("--upgrade", "-u", is_flag=True, default=False)
@click.argument("library_name", required=True)
def install_action_lib(library_name, upgrade):
    library_name = "https://github.com/openpipe-extra-actions/" + library_name
    download_and_cache(library_name, upgrade)
