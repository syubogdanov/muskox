import argparse
import multiprocessing
import pathlib

from muskox.cli import get_parser
from muskox.oxpath import fetch


def main():
    muskox: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = muskox.parse_args()

    oxpaths: set[str] = {args.lhs, args.rhs}.union(args.oxpaths)
    if len(oxpaths) < 2:
        muskox.error("The number of unique oxpaths must be at least two")

    threads: int = args.threads
    if threads <= 0:
        muskox.error("The number of threads must be positive")

    try:
        with multiprocessing.Pool(threads) as executor:
            paths: list[pathlib.Path] = executor.map(fetch, oxpaths)  # noqa

    except Exception as exception:
        muskox.error(exception)


if __name__ == "__main__":
    main()
