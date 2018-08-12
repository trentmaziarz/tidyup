#!/usr/bin/env python3
import argparse
import os
import shutil

DOWNLOADS = os.path.expanduser('~/Downloads')

RULES = {
    '.jpg': '~/Pictures/unsorted',
    '.jpeg': '~/Pictures/unsorted',
    '.png': '~/Pictures/unsorted',
    '.gif': '~/Pictures/unsorted',
    '.pdf': '~/Documents/pdf',
    '.zip': '~/Downloads/archives',
    '.tar.gz': '~/Downloads/archives',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--dry-run', action='store_true')
    args = parser.parse_args()

    for name in os.listdir(DOWNLOADS):
        ext = os.path.splitext(name)[1].lower()
        if ext not in RULES:
            continue
        dest = os.path.expanduser(RULES[ext])
        if args.dry_run:
            print('would move %s -> %s' % (name, dest))
            continue
        if not os.path.isdir(dest):
            os.makedirs(dest)
        shutil.move(os.path.join(DOWNLOADS, name), os.path.join(dest, name))
        print('moved', name)


if __name__ == '__main__':
    main()
