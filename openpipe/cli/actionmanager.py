import click
from os.path import dirname, join
from ..utils.download_cache import download_and_cache
from .run import pipeline_run


@click.command(name="install-actions-lib")
@click.option("--upgrade", "-u", is_flag=True, default=False)
@click.option("--auto-install", "-a", is_flag=True, default=False)
@click.argument("library_name", required=True)
def cmd_install_action_lib(library_name, upgrade, auto_install):
    """ Install an actions library """
    library_name = "https://github.com/openpipe-extra-actions/" + library_name
    download_and_cache(library_name, upgrade, auto_install)


@click.command(name="list-actions-lib")
def cmd_list_action_lib():
    """ List installable action libraries """
    command_pipeline_file = join(
        dirname(__file__), "pipelines", "list-actions-lib.yaml"
    )
    pipeline_run(command_pipeline_file)
