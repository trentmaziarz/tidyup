import os

from tidyup import mover
from tidyup.rules import Rule

DL = '/tmp/tidyup-test'


def test_unique_path(tmpdir):
    p = tmpdir.join('a.txt')
    assert mover.unique_path(str(p)) == str(p)
    p.write('x')
    assert mover.unique_path(str(p)) == str(tmpdir.join('a (1).txt'))
    tmpdir.join('a (1).txt').write('x')
    assert mover.unique_path(str(p)) == str(tmpdir.join('a (2).txt'))


def test_plan_and_move():
    open(os.path.join(DL, 'cat.jpg'), 'w').close()
    open(os.path.join(DL, 'notes.txt'), 'w').close()
    pics = os.path.join(DL, 'pics')
    rules = [Rule('images', ['*.jpg'], pics)]

    moves = mover.plan(DL, rules)
    assert moves == [(os.path.join(DL, 'cat.jpg'), os.path.join(pics, 'cat.jpg'))]

    for src, dest in moves:
        mover.move(src, dest)
    assert os.path.exists(os.path.join(pics, 'cat.jpg'))
    assert not os.path.exists(os.path.join(DL, 'cat.jpg'))
    assert os.path.exists(os.path.join(DL, 'notes.txt'))


def test_move_never_overwrites(tmpdir):
    src = tmpdir.join('a.txt')
    src.write('new')
    out = tmpdir.mkdir('out')
    out.join('a.txt').write('old')

    final = mover.move(str(src), str(out.join('a.txt')))
    assert final == str(out.join('a (1).txt'))
    assert out.join('a.txt').read() == 'old'
    assert out.join('a (1).txt').read() == 'new'
