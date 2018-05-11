import click
from .__version__ import __version__
from .kube import kube


@click.version_option(prog_name='hyperion-cli', version=__version__)
@click.group()
def main():
    """Command line tool to interact with BDR's Hyperion."""
    pass


main.add_command(kube)
