import os

import click

from . import __version__, mover
from .rules import load, ConfigError

DEFAULT_CONFIG = '~/.tidyup.yml'


def read_config(path):
    try:
        return load(os.path.expanduser(path))
    except ConfigError as e:
        raise click.ClickException(str(e))
    except IOError as e:
        raise click.ClickException('%s: %s' % (path, e.strerror))


@click.group()
@click.version_option(__version__)
def main():
    """Sort a downloads folder by rules in a YAML file."""


@main.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG, help='rules file')
@click.option('-n', '--dry-run', is_flag=True, help='show what would move and stop')
@click.option('-v', '--verbose', is_flag=True, help='print every move')
def run(config, dry_run, verbose):
    """Move files according to the rules."""
    target, rules = read_config(config)
    if verbose:
        click.echo('%d rules, target %s' % (len(rules), target))
    moves = mover.plan(target, rules)
    for src, dest in moves:
        if dry_run:
            click.echo('would move %s -> %s' % (src, dest))
            continue
        dest = mover.move(src, dest)
        if verbose:
            click.echo('%s -> %s' % (src, dest))


@main.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG, help='rules file')
def check(config):
    """Validate the rules file and exit."""
    target, rules = read_config(config)
    click.echo('%s: ok, %d rules' % (config, len(rules)))
