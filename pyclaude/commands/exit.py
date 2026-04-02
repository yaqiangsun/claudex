"""Exit command."""
import click

@click.command()
def exit_cmd():
    """Exit command."""
    click.echo("exit command")

__all__ = ['exit_cmd']