import click

#  import urllib.request
#  import os
#  from sys import stderr
from openpipe.client import PipelineFileLoader
from openpipe.pipeline.engine import PipelineManager
from os.path import exists
from wasabi import Printer

msg = Printer()


@click.command(name="run")
@click.option("--local-only", "-l", is_flag=True, default=False)
@click.option("--start-segment", "-s", type=str, default="start")
@click.argument("filename", type=click.Path(exists=False), required=True)
@click.argument("pipeline_arguments", nargs=-1)
def cmd_run(filename, pipeline_arguments, local_only, start_segment):
    if not exists(filename):
        msg.fail(f"File '{filename}' does not exist.")
        exit(1)
    pipeline_run(filename, pipeline_arguments, local_only, start_segment)


def pipeline_run(
    filename, pipeline_arguments=(), local_only=False, start_segment="start"
):

    # Fetch and validate the pipeline
    pipeline_loader = PipelineFileLoader()
    pipeline_loader.fetch(filename)
    pipeline_loader.validate()

    # Create a pipeline manager
    pipeline_manager = PipelineManager()
    pipeline_loader.load(pipeline_manager)

    # Runs the start method of all actions
    pipeline_manager.start()

    # Create links between actions
    pipeline_manager.create_action_links()

    # Send the activation element into the pipeline
    return pipeline_manager.activate(pipeline_arguments)
