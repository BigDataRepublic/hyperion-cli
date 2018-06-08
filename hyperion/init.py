import click
from shutil import copyfile
import os
import sys
from .common import render_jinja_template, write_file, read_yaml, cli_common_params
from .vars import *


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
    print(ASCII)
    print(f'Initializing project `{project_name}`...')

    # Read the kubeconfig file to find the username
    kubeconfig_path = kubeconfig if kubeconfig != '' else os.path.join(HOMEDIR, '.kube', 'config')
    try:
        kubeconfig_yml = read_yaml(kubeconfig_path)
    except IOError as e:
        print(f'ERROR: Could not find your kubectl configuration file at {kubeconfig_path}\n'
               'If your kubectl configuration file is in a different directory, '
               'please specify it with the --kubeconfig argument. ')
        sys.exit(1)

    # Find Hyperion username
    username = ''
    try:
        # Try to find the bdr_hyperion cluster definition in kubeconfig
        for context in kubeconfig_yml['contexts']:
            if context['context']['cluster'] == CLUSTER_NAME:
                username = context['context']['user']

        # Raise exception if username was not found
        if username == '':
            raise KeyError()
    except KeyError as e:
        print(f'ERROR: Could not find {CLUSTER_NAME} cluster definition in '
               'configuration file at {kubeconfig_path}')
        sys.exit(1)

    # Detect if there are already files present in this directory
    file_exists = check_existing_files()
    if file_exists is not None:
        print(f'ERROR: File ./{file_exists} already exists. Remove this file to '
               'continue.')
        sys.exit(1)

    click.echo('Generating Dockerfile...')
    copy_dockerfile()

    click.echo('Generating deployment.yml...')
    copy_deploymentyml(project_name, username)

    click.echo('Generating main.sh...')
    copy_mainsh()

    click.echo(f'Successfully created project {project_name}')
