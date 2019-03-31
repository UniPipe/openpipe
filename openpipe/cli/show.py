import click
from sys import exit
from wasabi import Printer
from ..utils import get_action_metadata, get_actions_metadata
from ..client.pretty import pretty_print_yaml

msg = Printer()


@click.command(name="show")
@click.argument("action_name", nargs=-1, required=True)
def cmd_show(action_name):
    action_name = " ".join(action_name)
    _ = get_actions_metadata()  # Just to force the path insert
    try:
        action = get_action_metadata(action_name, "show")
    except ModuleNotFoundError:
        msg.fail(f"No action module available for action name '{action_name}'")
        print("You can get the list of available actions with:")
        print("\topenpipe help")
        exit(2)
    print("### Pipeline Examples")
    pretty_print_yaml(action["test_filename"])
    print("### End Of Pipeline Examples")

