import click
import urllib.request
import os
from sys import stderr
from openpipe.engine import PipelineRuntime


@click.command()
@click.option('--local', '-l', is_flag=True, default=False)
@click.argument('filename', type=click.Path(exists=False), required=True)
def run(filename, local):
    if filename.startswith('http:') or filename.startswith('https:'):
        if local:
            print("ERROR: Attempting to load remote pipeline in !", file=stderr)
            exit(2)
        if filename.startswith('https://github.com'):
            filename += "?raw=1"
        local_filename, headers = urllib.request.urlretrieve(filename)
        pipeline = PipelineRuntime(local_filename, local=local)
        os.unlink(local_filename)
    else:
        pipeline = PipelineRuntime(filename, local=local)
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
