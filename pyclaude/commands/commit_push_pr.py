"""Commit-push-pr command."""
import click

@click.command()
def commit_push_pr():
    """Commit push PR command."""
    click.echo("commit-push-pr command")

__all__ = ['commit_push_pr']