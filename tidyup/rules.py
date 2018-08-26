import fnmatch
import os

import yaml


class Rule(object):

    def __init__(self, name, patterns, dest):
        self.name = name
        self.patterns = patterns
        self.dest = dest

    def matches(self, path):
        name = os.path.basename(path)
        if not any(fnmatch.fnmatch(name, p) for p in self.patterns):
            return False
        return True


def load(path):
    with open(path) as f:
        data = yaml.load(f)
    target = data['target']
    target = os.path.expanduser(target)

    rules = []
    for i, r in enumerate(data['rules']):
        patterns = r['match']
        if isinstance(patterns, str):
            patterns = [patterns]
        dest = r['dest']
        dest = os.path.expanduser(dest)
        if not os.path.isabs(dest):
            dest = os.path.join(target, dest)
        name = r.get('name', 'rule %d' % (i + 1))
        rules.append(Rule(name, patterns, dest))
    return target, rules
