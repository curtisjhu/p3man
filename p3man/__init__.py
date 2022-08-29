import click
from .account import reset, setup, wipe
from .queries import list, get, add, update

@click.group()
def cli():
    pass

cli.add_command(setup)
cli.add_command(reset)
cli.add_command(wipe)

cli.add_command(list)
cli.add_command(get)
cli.add_command(add)
cli.add_command(update)

