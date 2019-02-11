import click
import urllib.request
import os
from sys import stderr
from openpipe.engine import PipelineRuntime


@click.command()
@click.option('--local-only', '-l', is_flag=True, default=False)
@click.option('--start-segment', '-s', type=str, default="start")
@click.argument('filename', type=click.Path(exists=False), required=True)
def run(filename, local_only, start_segment):
    if filename.startswith('http:') or filename.startswith('https:'):
        if local_only:
            print("ERROR: Attempting to load remote pipeline in !", file=stderr)
            exit(2)
        if filename.startswith('https://github.com'):
            filename += "?raw=1"
        local_filename, headers = urllib.request.urlretrieve(filename)
        pipeline = PipelineRuntime(local_filename, local_only=local_only)
        os.unlink(local_filename)
    else:
        pipeline = PipelineRuntime(filename, local_only=local_only, start_segment=start_segment)
    pipeline.load()
    pipeline.start()
    pipeline.create_links()
    pipeline.activate()


def run_test(filename):
    pipeline = PipelineRuntime(filename)
    pipeline.load()
    pipeline.start()
    pipeline.create_links()
    return pipeline.activate()
