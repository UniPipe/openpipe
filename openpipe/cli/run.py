import click
#  import urllib.request
#  import os
#  from sys import stderr
from openpipe.core.loaders import PipelineFileLoader
from openpipe.pipeline.engine import PipelineManager


@click.command()
@click.option('--local-only', '-l', is_flag=True, default=False)
@click.option('--start-segment', '-s', type=str, default="start")
@click.argument('filename', type=click.Path(exists=False), required=True)
def run(filename, local_only, start_segment):
    """
    if filename.startswith('http:') or filename.startswith('https:'):
        if local_only:
            print("ERROR: Attempting to load remote pipeline in !", file=stderr)
            exit(2)
        if filename.startswith('https://github.com'):
            filename += "?raw=1"
        os.unlink(local_filename)
    else:
        pipeline_loader = PipelineFileLoader()
        pipeline = PipelineRuntime(filename, local_only=local_only, start_segment=start_segment)
    """
    pipeline_run(filename, local_only, start_segment)


def pipeline_run(filename, local_only=False, start_segment="start", report_error=True):

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
    return pipeline_manager.activate()
