import argparse
import enum
import pathlib

from muskox.package import name
from muskox.package import version

from muskox.web.typing import URL


class Command(enum.StrEnum):
    LOCAL = enum.auto()
    REMOTE = enum.auto()


class ArgumentParser(argparse.ArgumentParser):
    __slots__: tuple[str] = ()

    def __init__(self):
        super().__init__(
            prog=name,
            add_help=False,
        )

        super().add_argument(
            "-h",
            "--help",
            action="help",
            help="display the usage guide and exit",
        )

        super().add_argument(
            "-v",
            "--version",
            action="version",
            help="display the version and exit",
            version=version,
        )

        subparsers = super().add_subparsers(
            title="commands",
            parser_class=argparse.ArgumentParser,
            required=True,
            help="select the filesystem",
            dest="command",
        )

        local = subparsers.add_parser(
            name=Command.LOCAL,
            description="use the local filesystem",
            add_help=False,
        )

        local.add_argument(
            "-h",
            "--help",
            action="help",
            help="display the usage guide and exit",
        )

        local.add_argument(
            "path1",
            type=pathlib.Path,
            help="the path to the first object",
            metavar="PATH",
        )

        local.add_argument(
            "path2",
            type=pathlib.Path,
            help="the path to the second object",
            metavar="PATH",
        )

        remote = subparsers.add_parser(
            name=Command.REMOTE,
            description="use the remote filesystem",
            add_help=False,
        )

        remote.add_argument(
            "-h",
            "--help",
            action="help",
            help="display the usage guide and exit",
        )

        remote.add_argument(
            "url1",
            type=URL,
            help="the URL to the first object",
            metavar="URL",
        )

        remote.add_argument(
            "url2",
            type=URL,
            help="the URL to the second object",
            metavar="URL",
        )
