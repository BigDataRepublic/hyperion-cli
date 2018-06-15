import click

from .__version__ import __version__
from .init import init
from .dashboard import dashboard
from .submit import submit


@click.version_option(prog_name='hyperion-cli', version=__version__)
@click.group()
def main():
    """Command line tool to interact with BDR's Hyperion cluster."""
    pass


main.add_command(init)
main.add_command(dashboard)
main.add_command(submit)
