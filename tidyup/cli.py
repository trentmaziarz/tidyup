import argparse
import os
import sys

from . import mover
from .rules import load, ConfigError

DEFAULT_CONFIG = '~/.tidyup.yml'


def main():
    parser = argparse.ArgumentParser(prog='tidyup')
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG)
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('--check', action='store_true',
                        help='only validate the config')
    args = parser.parse_args()

    try:
        target, rules = load(os.path.expanduser(args.config))
    except ConfigError as e:
        sys.exit('tidyup: %s' % e)

    if args.check:
        print('%s: ok, %d rules' % (args.config, len(rules)))
        return

    for src, dest in mover.plan(target, rules):
        if args.dry_run:
            print('would move %s -> %s' % (src, dest))
        else:
            dest = mover.move(src, dest)
            print('%s -> %s' % (src, dest))


if __name__ == '__main__':
    main()
