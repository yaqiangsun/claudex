"""Pr-comments command."""
import click

@click.command()
def pr_comments():
    """PR comments command."""
    click.echo("pr-comments command")

__all__ = ['pr_comments']