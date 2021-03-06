import os
import re

import click
from shutil import copyfile

from .kube_util import hyperion_username
from .common import render_jinja_template, write_file, cli_common_params, \
    exit, exit_with_error, HyperionCLIException
from .vars import *


def verify_project_name(project_name):
    """
    Verify that we have a project name that can be used
    as a Docker image name
    """
    if re.fullmatch('[a-z, 0-9, \\-]*', project_name) is None:
        raise HyperionCLIException(
            'Project name may only contain lowercase a-z, '
            'numeric values and a dash (-)')


def copy_dockerfile():
    """
    Copies the template Dockerfile to the project folder.
    """
    src = os.path.join(REALPATH, 'res', 'Dockerfile')
    dest = os.path.join(CWD, 'Dockerfile')

    copyfile(src, dest)


def copy_mainsh():
    """
    Copies the template main.sh to the project folder.
    """
    src = os.path.join(REALPATH, 'res', 'main.sh')
    dest = os.path.join(CWD, 'main.sh')

    copyfile(src, dest)


def copy_modelpy():
    """
    Copies the template model.py to the project folder.
    """
    src = os.path.join(REALPATH, 'res', 'model.py')
    dest = os.path.join(CWD, 'model.py')
    if os.path.exists(dest):
        click.echo('Skipping model.py because it already exists')
    else:
        copyfile(src, dest)


def copy_deploymentyml(name, username):
    """
    Copy the jinja-rendered deployment.yml file to the project directory.
    """
    src = os.path.join(REALPATH, 'res', 'deployment.yml')
    dest = os.path.join(CWD, 'deployment.yml')

    templated = render_jinja_template(src, name=name, username=username)
    write_file(dest, templated)


def check_existing_files():
    """
    Checks if the files to be generated already exists. If any file does exist,
    return a string containing the file path. If no file exists, returns None.
    """
    for path in GENERATED_FILES:
        if os.path.isfile(path):
            return path

    return None


@click.command()
@click.argument('project_name')
@cli_common_params
def init(kubeconfig, project_name):
    """ Initializes a new Hyperion project """
    try:
        # First do some basic checks
        verify_project_name(project_name)
        username = hyperion_username(kubeconfig)
    except HyperionCLIException as exc:
        exit_with_error(exc)

    click.echo(ASCII)
    click.echo(f'Initializing project `{project_name}`...')

    # Detect if there are already files present in this directory
    file_exists = check_existing_files()
    if file_exists is not None:
        exit_with_error(
            f'ERROR: File ./{file_exists} already exists. Remove this file to continue.')

    click.echo('Generating Dockerfile...')
    copy_dockerfile()

    click.echo('Generating deployment.yml...')
    copy_deploymentyml(project_name, username)

    click.echo('Generating main.sh...')
    copy_mainsh()

    click.echo('Generating model.py...')
    copy_modelpy()

    exit(f'Successfully created project {project_name}')
