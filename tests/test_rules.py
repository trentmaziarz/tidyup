import os
import time

import pytest

from tidyup.rules import Rule, load, ConfigError


def write(tmpdir, text):
    p = tmpdir.join('rules.yml')
    p.write(text)
    return str(p)


def test_load_basic(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - name: images
    match: ["*.jpg", "*.png"]
    dest: /tmp/pics
""")
    target, rules = load(path)
    assert target == '/tmp/dl'
    assert len(rules) == 1
    assert rules[0].name == 'images'
    assert rules[0].patterns == ['*.jpg', '*.png']
    assert rules[0].dest == '/tmp/pics'


def test_match_can_be_one_string(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - match: "*.pdf"
    dest: /tmp/pdf
""")
    target, rules = load(path)
    assert rules[0].patterns == ['*.pdf']
    assert rules[0].name == 'rule 1'


def test_matches():
    r = Rule('x', ['*.jpg', '*.png'], '/tmp')
    assert r.matches('/a/b/c.jpg')
    assert r.matches('c.png')
    assert not r.matches('/a/b/c.txt')


def test_relative_dest_goes_under_target(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - match: "*.pdf"
    dest: pdf
""")
    target, rules = load(path)
    assert rules[0].dest == '/tmp/dl/pdf'


def test_older_than(tmpdir):
    f = tmpdir.join('setup.exe')
    f.write('x')
    r = Rule('old', ['*.exe'], '/tmp', older_than=30)
    assert not r.matches(str(f))

    past = time.time() - 40 * 86400
    os.utime(str(f), (past, past))
    assert r.matches(str(f))


def test_no_target(tmpdir):
    path = write(tmpdir, "rules: []\n")
    with pytest.raises(ConfigError):
        load(path)


def test_not_a_mapping(tmpdir):
    path = write(tmpdir, "- just\n- a list\n")
    with pytest.raises(ConfigError):
        load(path)


def test_rule_without_match(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - dest: /tmp/pics
""")
    with pytest.raises(ConfigError):
        load(path)


def test_case_insensitive():
    r = Rule('x', ['*.JPG'], '/tmp')
    assert r.matches('photo.jpg')
    assert r.matches('PHOTO.Jpg')


def test_trash_dest(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - match: "*.exe"
    dest: trash
""")
    target, rules = load(path)
    assert rules[0].dest == '/tmp/dl/.tidyup-trash'


def test_trailing_slash(tmpdir):
    path = write(tmpdir, """
target: /tmp/dl
rules:
  - match: "*.jpg"
    dest: /tmp/pics/
""")
    target, rules = load(path)
    assert rules[0].dest == '/tmp/pics'
