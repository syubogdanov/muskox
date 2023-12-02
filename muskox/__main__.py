import argparse
import multiprocessing
import pathlib

from muskox import cache
from muskox import cli
from muskox import oxpath


def main():
    muskox: argparse.ArgumentParser = cli.get_parser()
    args: argparse.Namespace = muskox.parse_args()

    oxpaths: set[str] = {args.lhs, args.rhs}.union(args.oxpaths)
    if len(oxpaths) < 2:
        muskox.error("The number of unique oxpaths must be at least two")

    threads: int = args.threads
    if threads <= 0:
        muskox.error("The number of threads must be positive")

    cache.clean()  # Note that cleanup must be performed before using threads

    try:
        with multiprocessing.Pool(threads) as executor:
            paths: list[pathlib.Path] = executor.map(oxpath.fetch, oxpaths)  # noqa

    except Exception as exception:
        muskox.error(exception)


if __name__ == "__main__":
    main()
