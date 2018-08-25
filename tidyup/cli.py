import argparse
import os

from . import mover
from .rules import load

DEFAULT_CONFIG = '~/.tidyup.yml'


def main():
    parser = argparse.ArgumentParser(prog='tidyup')
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG)
    parser.add_argument('-n', '--dry-run', action='store_true')
    args = parser.parse_args()

    target, rules = load(os.path.expanduser(args.config))

    for src, dest in mover.plan(target, rules):
        if args.dry_run:
            print('would move %s -> %s' % (src, dest))
        else:
            dest = mover.move(src, dest)
            print('%s -> %s' % (src, dest))


if __name__ == '__main__':
    main()
