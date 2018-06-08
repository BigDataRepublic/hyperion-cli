import click


@click.command()
def submit():
    """ Submits a project to be run on Hyperion """
    click.echo('Submit')
