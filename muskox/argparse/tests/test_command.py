from muskox.argparse import Command


def test_local():
    assert Command.LOCAL == "local"


def test_remote():
    assert Command.REMOTE == "remote"
