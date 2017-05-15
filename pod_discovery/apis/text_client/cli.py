"""Module with common db cli commands.

Exposes commands as a click group `basic_cmds`.
"""

import click
from pod_discovery.apis.text import TextClient

__all__ = ['cli']

_client = TextClient()


@click.command()
def _check_health():
    """Checks client health."""
    click.echo(_client.check_health())


@click.command()
@click.argument('pod_id')
def _get_pod(pod_id):
    """Get an pod by id."""
    click.echo(_client.get_pod(int(pod_id)))


_cmds = {
    'check_health': _check_health,
    'get_pod': _get_pod
}


class _GrpcPythonExampleTextClientCli(click.MultiCommand):
    def list_commands(self, ctx):
        return sorted(list(_cmds.keys()))

    def get_command(self, ctx, name):
        return _cmds[name]


cli = _GrpcPythonExampleTextClientCli(help='Text client commands')
