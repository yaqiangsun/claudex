"""Perf-issue command."""
import click

@click.command()
def perf_issue():
    """Perf issue command."""
    click.echo("perf-issue command")

__all__ = ['perf_issue']