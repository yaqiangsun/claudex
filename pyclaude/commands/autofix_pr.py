"""Autofix-pr command."""
import click

@click.command()
def autofix_pr():
    """Autofix PR command."""
    click.echo("autofix-pr command")

__all__ = ['autofix_pr']