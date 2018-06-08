import os


CLUSTER_NAME = 'bdr_hyperion'
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
