import click
from .account import update, setup
from .queries import list, retrieve

@click.group()
def cli():
    pass
cli.add_command(update)
cli.add_command(list)
cli.add_command(setup)
cli.add_command(retrieve)

