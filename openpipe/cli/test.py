import click
from sys import stderr, exit
from .run import pipeline_run
from ..utils import get_actions_metadata
from ..client.pretty import pretty_print_yaml


@click.command(name="test")
@click.option("--print-source", "-p", is_flag=True, default=False)
@click.argument("action_name", nargs=-1, required=True)
def cmd_test(action_name, print_source):
    action_name = " ".join(action_name)
    action = [action for action in get_actions_metadata() if action['name'] == action_name]
    if not action:
        print("No action found for name '%s'" % action_name, file=stderr)
        exit(2)
    action = action[0]
    if print_source:
        print("### Pipeline Source")
        pretty_print_yaml(action['test_file_name'])
        print("### End Of Pipeline Source")
    print("### Pipeline Execution:")
    pipeline_run(action['test_file_name'], False, "start")
