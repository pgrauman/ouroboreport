import os

from ouroboreport.shared import ifnotexistmkdir


def test_ifnotexistmkdir(tmpdir):
    newdir = tmpdir / "test_new"
    newdir_made = ifnotexistmkdir(newdir)
    assert newdir_made == newdir
    assert os.path.exists(newdir_made)
