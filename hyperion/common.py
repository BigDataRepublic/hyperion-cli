import sys
import click
from jinja2 import Template
import yaml
import functools


class HyperionCLIException(Exception):
    pass


def render_jinja_template(path, **kwargs):
    """
    Reads a jinja2 template, renders it, and returns the rendered string.
    """
    with open(path) as file:
        template = Template(file.read())
    return template.render(**kwargs)


def write_file(path, content):
    """
    Writes a string to a file.
    """
    with open(path, 'w') as file:
        file.write(content)


def read_yaml(path):
    """
    Reads a yml file and returns it as a string.
    """
    with open(path) as file:
        return yaml.load(file)


def cli_common_params(func):
    @click.option('--kubeconfig', default=None, help='Path to your kubectl config file.')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def exit_with_error(msg=''):
    click.secho(f'ERROR: {msg}', err=True, fg='red')
    sys.exit(1)


def exit(msg='', text_color='green'):
    if msg:
        click.secho(msg, fg=text_color)
    sys.exit(0)
