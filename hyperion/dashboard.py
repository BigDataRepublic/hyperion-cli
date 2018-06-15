from subprocess import Popen, DEVNULL, PIPE, check_call, CalledProcessError

import click

from .vars import CLUSTER_NAME, DASHBOARD_URL
from .common import cli_common_params, exit, exit_with_error, HyperionCLIException
from .kube_util import kubectl_version, kube_client


@click.command()
@cli_common_params
def dashboard(kubeconfig):
    """ Starts the Kubernetes Dashboard """
    try:
        kubectl_version()
        hyperion_context, hyperion_client = kube_client(kubeconfig)
    except HyperionCLIException as exc:
        exit_with_error(exc)

    if CLUSTER_NAME == 'minikube':
        dashboard_token = 'TOKEN NOT REQUIRED'
    else:
        username = hyperion_context['context']['user']
        user_namespace = hyperion_context['context']['namespace']
        user_namespace_secrets = hyperion_client.list_namespaced_secret(
            user_namespace,
            pretty=True,
            watch=False).items
        dashboard_secret = next(x for x in user_namespace_secrets if
                                x.metadata.annotations['kubernetes.io/service-account.name'] ==
                                f'dashboard-{username}')
        dashboard_token = dashboard_secret.data['token']

    try:
        context_name = hyperion_context['name']
        check_call(['kubectl', 'config', 'use-context', context_name], stdout=DEVNULL)
    except CalledProcessError:
        exit_with_error(f'Could not switch the context to {context_name}')

    try:
        click.echo(f'Open your browser and go to {DASHBOARD_URL}\n\n' +
                   f'When asked for login, use {dashboard_token}')
        proxy_process = Popen(['kubectl', 'proxy'], stdout=DEVNULL, stderr=PIPE)

        # communicate() blocks until the process has exited. In our case, it only exits
        # automatically on error.
        _, err = proxy_process.communicate()
        exit_with_error(f'Could not start proxy:\n{err}\nExiting...')
    except KeyboardInterrupt:
        exit('Exiting...')
        proxy_process.kill()  # Kill it with fire, asap
