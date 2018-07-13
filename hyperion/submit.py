import click
from .vars import *
import subprocess
from .common import exit_with_error, cli_common_params, HyperionCLIException
from .kube_util import hyperion_username
from .deployment_util import load_deployment


def kubectl_apply(deployment_file):
    #TODO Use kubernetes client library for this
    if not os.path.isfile(deployment_file):
        exit_with_error(
            f'ERROR: File "{deployment_file}" is missing, maybe run hyperion init first?')
    subprocess.run(["kubectl", "apply", "-f", deployment_file])

def docker_tag(username, project_name):
    return f"10.8.0.1:30000/{username}/{project_name}:latest"

def docker_build_command(tag):
    return [
        "docker",
        "build",
        "--tag",
        tag,
        "."
        ]

def docker_push_command(tag):
    return [
        "docker",
        "push",
        tag
        ]
# if failed to register layer: devmapper: Thin Pool has 148808 free data blocks which is less than minimum required 163840 free data blocks. Create more free space in thin pool or use dm.min_free_space option to change behavior
# send user to https://github.com/rhcarvalho/openshift-devtools/blob/master/docker-cleanup
def docker_build(username, project_name):
    dockerfile = os.path.join(CWD, 'Dockerfile')

    if not os.path.isfile(dockerfile):
        exit_with_error(
            f'ERROR: File "{dockerfile}" is missing, maybe run hyperion init first?')
    tag_name = docker_tag(username, project_name)
    build_proc = subprocess.run(docker_build_command(tag_name))
    if not build_proc.returncode == 0:
        exit_with_error(f'Docker build process failed, stopping')

def docker_push(username, project_name):
    tag_name = docker_tag(username, project_name)
    push_proc = subprocess.run(docker_push_command(tag_name))
    if not push_proc.returncode == 0:
        exit_with_error(f'Docker push process failed, stopping')

@click.command()
@cli_common_params
def submit(kubeconfig):
    """ Submits a project to be run on Hyperion """
    click.echo(ASCII)
    try:
        username = hyperion_username(kubeconfig)
        deployment_config = load_deployment()
        project_name = deployment_config['metadata']['name']
        docker_build(username, project_name)
        docker_push(username, project_name)
        #TODO Clean up namespace with to allow for redeployment
        kubectl_apply("deployment.yml")
        click.echo("Tip: visit your job using: hyperion dashboard")
    except HyperionCLIException as exc:
        exit_with_error(exc)
