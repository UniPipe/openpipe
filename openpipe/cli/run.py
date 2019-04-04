import click

#  import urllib.request
#  import os
#  from sys import stderr
from openpipe.client import PipelineFileLoader
from openpipe.pipeline.engine import PipelineManager
from os.path import exists, abspath, dirname
from os import environ
from wasabi import Printer

msg = Printer()


@click.command(name="run")
@click.option(
    "--network-enable",
    "-n",
    is_flag=True,
    default=False,
    help="automatically download libraries from https",
)
@click.option("--start-segment", "-s", type=str, default="start")
@click.argument("filename", type=click.Path(exists=False), required=True)
@click.argument("pipeline_arguments", nargs=-1)
def cmd_run(filename, pipeline_arguments, network_enable, start_segment):
    """ Run a pipeline  """
    if not exists(filename):
        msg.fail(f"File '{filename}' does not exist.")
        exit(1)
    environ["OPENPIPE_AUTO_NETWORK"] = str(network_enable)
    pipeline_run(filename, pipeline_arguments, start_segment=start_segment)


def pipeline_run(filename, pipeline_arguments=(), start_segment="start"):

    # Fetch and validate the pipeline
    pipeline_loader = PipelineFileLoader()
    pipeline_loader.fetch(filename)
    pipeline_loader.validate(start_segment=start_segment)

    # Create a pipeline manager
    pipeline_manager = PipelineManager(start_segment)
    pipeline_loader.load(pipeline_manager, start_segment=start_segment)

    # Runs the start method of all actions
    pipeline_manager.start()

    # Create links between actions
    pipeline_manager.create_action_links()

    # Send the activation element to the pipeline start segment
    path = abspath(dirname(filename))
    activation_item = {"path": path, "name": filename, "arguments": pipeline_arguments}
    return pipeline_manager.activate(activation_item)
