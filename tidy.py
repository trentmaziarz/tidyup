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


def unique(path):
    # foo.jpg -> foo (1).jpg, not foo.jpg (1)
    base, ext = os.path.splitext(path)
    n = 1
    while os.path.exists(path):
        path = '%s (%d)%s' % (base, n, ext)
        n += 1
    return path


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
            final = unique(os.path.join(dest, name))
            shutil.move(os.path.join(target, name), final)
            print('moved %s -> %s' % (name, final))
            break


if __name__ == '__main__':
    main()
