import click


@click.command()
def dashboard():
    """ Starts the Kubernetes Dashboard """
    click.echo('Dashboard')
