import click
import urllib.request
import os
from openpipe.engine import PipelineRuntime


@click.command()
@click.argument('filename', type=click.Path(exists=False), nargs=-1, required=True)
def run(filename):
    filename = filename[0]
    if filename.startswith('http:') or filename.startswith('https:'):
        if filename.startswith('https://github.com'):
            filename += "?raw=1"
        local_filename, headers = urllib.request.urlretrieve(filename)
        pipeline = PipelineRuntime(local_filename)
        os.unlink(local_filename)
    else:
        pipeline = PipelineRuntime(filename)
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
