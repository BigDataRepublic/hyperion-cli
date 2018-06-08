import click
import os
from shutil import copyfile


def copy_dockerfile():
    src = os.path.dirname(os.path.realpath(__file__)) + '/res/Dockerfile'
    dest = os.getcwd() + '/Dockerfile'

    copyfile(src, dest)


@click.command()
@click.argument('name')
def init(name):
    """ Initializes a new Hyperion project """
    click.echo('Generating Dockerfile...')
    copy_dockerfile()

    click.echo('Generating deployment.yml')
    

    click.echo('Check if kube config is in place...')
    click.echo('Create main.sh')

@click.command()
def dashboard():
    """ Starts the Kubernetes Dashboard """
    click.echo('Dashboard')

@click.command()
def submit():
    """ Submits a project to be run on Hyperion """
    click.echo('Submit')
