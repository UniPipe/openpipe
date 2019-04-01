import click
from sys import exit
from wasabi import Printer
from .run import pipeline_run
from ..utils import get_action_metadata
from ..client.pretty import pretty_print_yaml

msg = Printer()


@click.command(name="test")
@click.option("--print-source", "-p", is_flag=True, default=False)
@click.argument("action_name", nargs=-1, required=True)
def cmd_test(action_name, print_source):
    """ Run tests for an action"""
    action_name = " ".join(action_name)
    try:
        action = get_action_metadata(action_name, "test")
    except ModuleNotFoundError:
        msg.fail(f"No action module available for action name '{action_name}'")
        print("You can get the list of available actions with:")
        print("\topenpipe help")
        exit(2)
    if print_source:
        print("### Pipeline Source")
        pretty_print_yaml(action["test_filename"])
        print("### End Of Pipeline Source")
    print("### Pipeline Execution:")
    pipeline_run(action["test_filename"])
