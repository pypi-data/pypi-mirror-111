"""Console script for nin."""
import sys
import click

import sys

from nin import cli_dns

@click.group()
@click.pass_context
def main(args=None):
    return 0

main.add_command(cli_dns.dns)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
