import click


@click.group()
def kube():
    """Kubernetes interactions."""
    pass


@click.command()
def dashboard():
    click.echo('Hello dashboard')


kube.add_command(dashboard)
