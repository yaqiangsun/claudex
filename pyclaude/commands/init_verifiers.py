"""Init-verifiers command."""
import click

@click.command()
def init_verifiers():
    """Init verifiers command."""
    click.echo("init-verifiers command")

__all__ = ['init_verifiers']