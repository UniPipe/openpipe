import click
from ..utils.download_cache import download_and_cache


@click.command(name="install-plugin")
@click.option("--upgrade", "-u", is_flag=True, default=False)
@click.argument("plugin_name", required=True)
def install_plugin(plugin_name, upgrade):
    library_name = "https://github.com/openpipe-plugins/" + plugin_name
    download_and_cache(library_name, upgrade)
