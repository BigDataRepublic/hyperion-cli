import yaml
from .common import HyperionCLIException

def load_deployment():
    try:
        with open("./deployment.yml") as deployment_file:
            return yaml.load(deployment_file)
    except FileNotFoundError as e:
        raise HyperionCLIException(
            'Could not load deployment.yml file')
