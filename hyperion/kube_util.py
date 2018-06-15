from subprocess import check_call, CalledProcessError

from kubernetes import client, config

from .vars import CLUSTER_NAME
from .common import HyperionCLIException


def kubectl_version():
    try:
        check_call(['kubectl', 'version'])
    except CalledProcessError:
        raise HyperionCLIException('kubectl is not installed')


def kube_client(kubeconfig: str):
    """Find the hyperion cluster context and return a ready-to-use kube client"""
    try:
        contexts, active_context = config.list_kube_config_contexts(kubeconfig)
        hyperion_context = next(x for x in contexts if x['context']['cluster'] == CLUSTER_NAME)
        return hyperion_context, client.CoreV1Api(
            api_client=config.new_client_from_config(context=hyperion_context['name']))
    except StopIteration:
        raise HyperionCLIException(
            'Could not find a hyperion context. Please check you kube config.')


def submit_job():
    pass
