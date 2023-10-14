import pathlib
import random

import pytest

from muskox.argparse import ArgumentParser
from muskox.argparse import Command

from muskox.package import name

from muskox.utils.string import random_string

from muskox.web.typing import URL


ITERATIONS: int = 1024
RANDOM_ARGS_MAXCOUNT: int = 128


@pytest.fixture
def parser() -> ArgumentParser:
    return ArgumentParser()


def test_empty_command(parser: ArgumentParser):
    with pytest.raises(SystemExit) as subprocess:
        parser.parse_args([])

    assert subprocess.value.code == 2


def test_unknown_command(parser: ArgumentParser):
    for _ in range(ITERATIONS):
        command: str = random_string()

        if command in {Command.LOCAL, Command.REMOTE}:
            continue

        arg1: str = random_string()
        arg2: str = random_string()

        with pytest.raises(SystemExit) as subprocess:
            parser.parse_args([command, arg1, arg2])

        assert subprocess.value.code == 2


def test_local_command_ok_arguments(parser: ArgumentParser):
    for _ in range(ITERATIONS):

        path1: str = random_string()
        path2: str = random_string()

        args = parser.parse_args(["local", path1, path2])
        assert args.command == Command.LOCAL

        assert args.path1 == pathlib.Path(path1)
        assert args.path2 == pathlib.Path(path2)


def test_local_command_without_arguments(parser: ArgumentParser):
    with pytest.raises(SystemExit) as subprocess:
        parser.parse_args(["local"])

    assert subprocess.value.code == 2


def test_local_command_one_argument(parser: ArgumentParser):
    with pytest.raises(SystemExit) as subprocess:
        path: str = random_string()
        parser.parse_args(["local", path])

    assert subprocess.value.code == 2


def test_local_command_excess_arguments(parser: ArgumentParser):
    for _ in range(ITERATIONS):

        count: int = random.randint(3, RANDOM_ARGS_MAXCOUNT)
        args = ["local"] + [random_string() for _ in range(count)]

        with pytest.raises(SystemExit) as subprocess:
            parser.parse_args(args)

        assert subprocess.value.code == 2


def test_remote_command_ok_arguments(parser: ArgumentParser):
    for _ in range(ITERATIONS):

        url1: str = random_string()
        url2: str = random_string()

        args = parser.parse_args(["remote", url1, url2])
        assert args.command == Command.REMOTE

        assert args.url1 == URL(url1)
        assert args.url2 == URL(url2)


def test_remote_command_without_arguments(parser: ArgumentParser):
    with pytest.raises(SystemExit) as subprocess:
        parser.parse_args(["remote"])

    assert subprocess.value.code == 2


def test_remote_command_one_argument(parser: ArgumentParser):
    with pytest.raises(SystemExit) as subprocess:
        url: str = random_string()
        parser.parse_args(["remote", url])

    assert subprocess.value.code == 2


def test_remote_command_excess_arguments(parser: ArgumentParser):
    for _ in range(ITERATIONS):

        count: int = random.randint(3, RANDOM_ARGS_MAXCOUNT)
        args = ["remote"] + [random_string() for _ in range(count)]

        with pytest.raises(SystemExit) as subprocess:
            parser.parse_args(args)

        assert subprocess.value.code == 2


def test_prog(parser: ArgumentParser):
    assert parser.prog == name


@pytest.mark.parametrize(
    argnames="args",
    argvalues=(
        ["-h"],
        ["--help"],
        ["local", "-h"],
        ["local", "--help"],
        ["remote", "-h"],
        ["remote", "--help"],
    )
)
def test_help(parser: ArgumentParser, args: list[str]):
    with pytest.raises(SystemExit) as subprocess:
        parser.parse_args(args)

    assert subprocess.value.code == 0


@pytest.mark.parametrize(
    argnames="args",
    argvalues=(
        ["-v"],
        ["--version"],
    )
)
def test_version(parser: ArgumentParser, args: list[str]):
    with pytest.raises(SystemExit) as subprocess:
        parser.parse_args(args)

    assert subprocess.value.code == 0


@pytest.mark.parametrize(
    argnames="command, prefix",
    argvalues=(
        ["local", "-"],
        ["local", "--"],
        ["remote", "-"],
        ["remote", "--"],
    )
)
def test_unknown_option(parser: ArgumentParser, command: str, prefix: str):
    for _ in range(ITERATIONS):

        option: str = prefix + random_string()
        if option in {"-h", "--help", "-v", "--version"}:
            continue

        arg1: str = random_string()
        arg2: str = random_string()

        with pytest.raises(SystemExit) as subprocess:
            parser.parse_args([command, arg1, arg2, option])

        assert subprocess.value.code == 2
