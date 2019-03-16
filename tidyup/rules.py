import fnmatch
import os
import time

import yaml

TRASH = '.tidyup-trash'


class ConfigError(Exception):
    pass


class Rule(object):

    def __init__(self, name, patterns, dest, older_than=None):
        self.name = name
        self.patterns = patterns
        self.dest = dest
        self.older_than = older_than

    def matches(self, path):
        name = os.path.basename(path)
        # fnmatch.fnmatch only ignores case on windows
        name = name.lower()
        if not any(fnmatch.fnmatchcase(name, p.lower()) for p in self.patterns):
            return False
        if self.older_than is not None:
            age = (time.time() - os.path.getmtime(path)) / 86400.0
            if age < self.older_than:
                return False
        return True


def load(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ConfigError('%s: expected a mapping at the top level' % path)
    if 'target' not in data:
        raise ConfigError('%s: no target' % path)
    target = data['target']
    target = os.path.expanduser(target)

    rules = []
    for i, r in enumerate(data.get('rules') or []):
        if 'match' not in r:
            raise ConfigError('rule %d: no match' % (i + 1))
        if 'dest' not in r:
            raise ConfigError('rule %d: no dest' % (i + 1))
        patterns = r['match']
        if isinstance(patterns, str):
            patterns = [patterns]
        dest = r['dest']
        dest = dest.rstrip('/')
        if dest == 'trash':
            dest = TRASH
        dest = os.path.expanduser(dest)
        if not os.path.isabs(dest):
            dest = os.path.join(target, dest)
        name = r.get('name', 'rule %d' % (i + 1))
        rules.append(Rule(name, patterns, dest, r.get('older_than')))
    return target, rules
