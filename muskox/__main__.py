import argparse
import pathlib

from muskox import oxpath


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("muskox")

    parser.add_argument(
        "lhs",
        help="the oxpath to the first object",
        metavar="OXPATH",
    )

    parser.add_argument(
        "rhs",
        help="the oxpath to the second object",
        metavar="OXPATH",
    )

    return parser


def main():
    muskox: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = muskox.parse_args()

    try:
        lhs: pathlib.Path = oxpath.fetch(args.lhs)  # noqa
        rhs: pathlib.Path = oxpath.fetch(args.rhs)  # noqa

    except Exception as exception:
        muskox.error(exception)


if __name__ == "__main__":
    main()
