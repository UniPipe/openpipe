import click
from sys import stderr, exit
from .run import pipeline_run
from ..utils import get_action_metadata, get_actions_metadata
from ..client.pretty import pretty_print_yaml


@click.command(name="test")
@click.option("--print-source", "-p", is_flag=True, default=False)
@click.argument("action_name", nargs=-1, required=True)
def cmd_test(action_name, print_source):
    action_name = " ".join(action_name)
    _ = get_actions_metadata()  # Just to force the path insert
    try:
        action = get_action_metadata(action_name, "test")
    except ModuleNotFoundError:
        print(
            "No action module available for action name '%s'" % action_name, file=stderr
        )
        exit(2)
    if print_source:
        print("### Pipeline Source")
        pretty_print_yaml(action["test_filename"])
        print("### End Of Pipeline Source")
    print("### Pipeline Execution:")
    pipeline_run(action["test_filename"], (), False, "start")
