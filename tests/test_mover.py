import os

from tidyup import mover
from tidyup.rules import Rule


def test_unique_path(tmpdir):
    p = tmpdir.join('a.txt')
    assert mover.unique_path(str(p)) == str(p)
    p.write('x')
    assert mover.unique_path(str(p)) == str(tmpdir.join('a (1).txt'))
    tmpdir.join('a (1).txt').write('x')
    assert mover.unique_path(str(p)) == str(tmpdir.join('a (2).txt'))


def test_plan_and_move(tmpdir):
    dl = tmpdir.mkdir('dl')
    dl.join('cat.jpg').write('x')
    dl.join('notes.txt').write('x')
    pics = str(tmpdir.join('pics'))
    rules = [Rule('images', ['*.jpg'], pics)]

    moves = mover.plan(str(dl), rules)
    assert moves == [(str(dl.join('cat.jpg')), os.path.join(pics, 'cat.jpg'))]

    for src, dest in moves:
        mover.move(src, dest)
    assert os.path.exists(os.path.join(pics, 'cat.jpg'))
    assert not dl.join('cat.jpg').check()
    assert dl.join('notes.txt').check()


def test_move_never_overwrites(tmpdir):
    src = tmpdir.join('a.txt')
    src.write('new')
    out = tmpdir.mkdir('out')
    out.join('a.txt').write('old')

    final = mover.move(str(src), str(out.join('a.txt')))
    assert final == str(out.join('a (1).txt'))
    assert out.join('a.txt').read() == 'old'
    assert out.join('a (1).txt').read() == 'new'


def test_skips_dirs_and_dotfiles(tmpdir):
    dl = tmpdir.mkdir('dl')
    dl.mkdir('folder.jpg')
    dl.join('.hidden.jpg').write('x')
    dl.join('real.jpg').write('x')
    rules = [Rule('images', ['*.jpg'], str(tmpdir.join('pics')))]

    moves = mover.plan(str(dl), rules)
    assert [os.path.basename(src) for src, dest in moves] == ['real.jpg']
