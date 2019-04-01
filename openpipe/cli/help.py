import click
from wasabi import Printer, color
from terminaltables import SingleTable
from ..utils import get_actions_metadata

msg = Printer()


@click.command(name="help")
@click.argument("action", nargs=-1, required=False)
def cmd_help(action):
    """ List available actions  """
    if len(action) == 0:
        return print_list_of_actions()

    action_name = " ".join(action)
    action = [
        action for action in get_actions_metadata() if action["name"] == action_name
    ]
    if not action:
        msg.fail(f"No action with name '{action_name}'")
        print("You can get the list of available actions with:")
        print("\topenpipe help")
        exit(2)
    action = action[0]

    #  pretty_print_yaml(examples_filename)
    print(color("PURPOSE", bold=True))
    print(f"\t{action['purpose']}")
    required_some_config = action.get("required_some_config")
    if required_some_config:
        print(color("\n# REQUIRED CONFIG", bold=True))
        print(f"    - {action_name}: ", end="")
        for line in required_some_config.splitlines():
            print(line)
    required_config = action.get("required_config")
    if required_config:
        print(color("\n# REQUIRED CONFIG", bold=True))
        print(f"    - {action_name}:")
        for line in required_config.splitlines():
            print(line)
    optional_config = action.get("optional_config")
    if optional_config:
        print(color("\n# OPTIONAL CONFIG", bold=True))
        if not required_config and not required_some_config:
            print(f"    - {action_name}:")
        for line in optional_config.splitlines():
            print(line)
    print(f"\nYou can see usage examples with:\n    openpipe show {action_name}")


def print_list_of_actions():

    table_data = [["Action Name", "Purpose"]]
    for action_metadata in get_actions_metadata():
        table_data.append((action_metadata["name"], action_metadata["purpose"]))
    table = SingleTable(table_data)
    print(table.table)
    print("You can get help for an action with:")
    print("\topenpipe help «action_name»")
