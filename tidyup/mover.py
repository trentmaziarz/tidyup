import os
import shutil


def unique_path(path):
    """foo.jpg -> foo (1).jpg if foo.jpg is taken"""
    base, ext = os.path.splitext(path)
    n = 1
    while os.path.exists(path):
        path = '%s (%d)%s' % (base, n, ext)
        n += 1
    return path


def candidates(target):
    for name in sorted(os.listdir(target)):
        path = os.path.join(target, name)
        yield path


def plan(target, rules):
    """list of (src, dest) for everything a rule wants moved"""
    moves = []
    for path in candidates(target):
        for rule in rules:
            if rule.matches(path):
                moves.append((path, os.path.join(rule.dest, os.path.basename(path))))
                break
    return moves


def move(src, dest):
    """move src to dest without overwriting anything. returns the final path"""
    folder = os.path.dirname(dest)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    dest = unique_path(dest)
    shutil.move(src, dest)
    return dest
