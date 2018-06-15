import os

DEFAULT_CLUSTER_NAME = 'bdr-hyperion'
CLUSTER_NAME = os.getenv('CLUSTER_NAME', DEFAULT_CLUSTER_NAME)
GENERATED_FILES = ['Dockerfile', 'main.sh', 'deployment.yml']
ASCII = '''
    __  __                      _
   / / / /_  ______  ___  _____(_)___  ____
  / /_/ / / / / __ \/ _ \/ ___/ / __ \/ __ \\
 / __  / /_/ / /_/ /  __/ /  / / /_/ / / / /
/_/ /_/\__, / .___/\___/_/  /_/\____/_/ /_/
      /____/_/
'''
CWD = os.getcwd()
REALPATH = os.path.dirname(os.path.realpath(__file__))
HOMEDIR = os.path.expanduser("~")
DASHBOARD_BASE_URL = 'http://localhost:8001/api/v1/namespaces/kube-system/services/'
DASHBOARD_URL = \
    f'{DASHBOARD_BASE_URL}https:kubernetes-dashboard:/proxy/' \
    if CLUSTER_NAME == DEFAULT_CLUSTER_NAME else \
    f'{DASHBOARD_BASE_URL}kubernetes-dashboard/proxy/#!/overview?namespace=default'
