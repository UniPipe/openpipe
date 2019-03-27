import click
from ..utils.download_cache import download_and_cache


@click.command(name="install-plugin")
@click.argument("plugin_name", required=True)
def install_plugin(plugin_name):
    library_name = "https://github.com/openpipe-plugins/" + plugin_name
    download_and_cache(library_name)
