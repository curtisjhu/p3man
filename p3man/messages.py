import click
def Error(m="An error occurred"):
	click.echo(click.style(m, fg="red"))
def ErrorWrongPassword():
	Error("Wrong Password.")
def Success(m = "Success!"):
	click.echo(click.style(m, fg="green"))