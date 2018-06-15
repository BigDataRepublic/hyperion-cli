from subprocess import check_call, CalledProcessError, DEVNULL

from kubernetes import client, config

from .vars import CLUSTER_NAME
from .common import HyperionCLIException


def kubectl_version():
    try:
        check_call(['kubectl', 'version'], stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError:
        raise HyperionCLIException('kubectl is not installed')


def _hyperion_context(kubeconfig: str):
    try:
        contexts, _ = config.list_kube_config_contexts(kubeconfig)
        return next(x for x in contexts if x['context']['cluster'] == CLUSTER_NAME)
    except StopIteration:
        raise HyperionCLIException(
            'Could not find a hyperion context. Please check you kube config.')
    except FileNotFoundError:
        raise HyperionCLIException(f'Kube config cannot be fount at {kubeconfig}')


def hyperion_context_name(kubeconfig: str):
    return _hyperion_context(kubeconfig)['name']


def hyperion_username(kubeconfig: str):
    return _hyperion_context(kubeconfig)['context']['user']


def hyperion_user_namespace(kubeconfig: str):
    return _hyperion_context(kubeconfig)['context']['namespace']


def hyperion_kube_client(kubeconfig: str):
    """Find the hyperion cluster context and return a ready-to-use kube client"""
    kube_client = config.new_client_from_config(
        config_file=kubeconfig, context=_hyperion_context(kubeconfig)['name'])
    return client.CoreV1Api(api_client=kube_client)


def submit_job():
    pass
