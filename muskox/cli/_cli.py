import argparse


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
        metavar="...",
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
