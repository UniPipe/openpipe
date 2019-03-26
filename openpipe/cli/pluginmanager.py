import click


@click.command(name="install-plugin")
@click.argument("plugin_name", required=True)
def install_plugin(plugin_name):
    print(plugin_name)
