import click
from openpipe.engine import PipelineRuntime


@click.command()
@click.argument('filename', type=click.Path(exists=False), nargs=-1, required=True)
def run(filename):
    pipeline = PipelineRuntime(filename[0])
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
