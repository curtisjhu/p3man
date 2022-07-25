import click

def print_terminal(pws: any):
    for a in pws:
        click.echo(f'{a[0]}: {a[1]}')
