#!/usr/bin/env python3
import argparse
import fnmatch
import os
import shutil

import yaml

CONFIG = os.path.expanduser('~/.tidyup.yml')


def load():
    with open(CONFIG) as f:
        return yaml.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--dry-run', action='store_true')
    args = parser.parse_args()

    config = load()
    target = os.path.expanduser(config['target'])

    for name in os.listdir(target):
        for rule in config['rules']:
            if not any(fnmatch.fnmatch(name, p) for p in rule['match']):
                continue
            dest = os.path.expanduser(rule['dest'])
            if args.dry_run:
                print('would move %s -> %s' % (name, dest))
                break
            if not os.path.isdir(dest):
                os.makedirs(dest)
            shutil.move(os.path.join(target, name), os.path.join(dest, name))
            print('moved', name)
            break


if __name__ == '__main__':
    main()
