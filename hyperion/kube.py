import click


@click.command()
def init():
    click.echo('Init')

@click.command()
def dashboard():
    click.echo('Dashboard')

@click.command()
def submit():
    click.echo('Submit')
