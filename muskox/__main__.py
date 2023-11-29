import argparse
import multiprocessing
import pathlib

from muskox.oxpath import fetch


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

    parser.add_argument(
        "oxpaths",
        nargs=argparse.REMAINDER,
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "-t",
        "--threads",
        default=16,
        type=int,
        help="the maximum number of threads",
        metavar="N",
    )

    return parser


def main():
    muskox: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = muskox.parse_args()

    oxpaths: list[str] = [args.lhs, args.rhs] + args.oxpaths
    threads: int = args.threads

    try:
        with multiprocessing.Pool(threads) as executor:
            paths: list[pathlib.Path] = executor.map(fetch, oxpaths)  # noqa

    except Exception as exception:
        muskox.error(exception)


if __name__ == "__main__":
    main()
