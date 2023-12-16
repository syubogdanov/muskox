import argparse
import multiprocessing
import pathlib

from muskox import cache
from muskox import cli
from muskox import oxpath

from muskox.estimators import damerau_levenshtein
from muskox.estimators import jaccard
from muskox.estimators import jaro_winkler
from muskox.estimators import jaro
from muskox.estimators import levenshtein


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

    pairs: list[tuple[pathlib.Path, pathlib.Path]] = []

    for lhs_index in range(len(paths) - 1):
        for rhs_index in range(lhs_index + 1, len(paths)):
            lhs = paths[lhs_index]
            rhs = paths[rhs_index]

            if not lhs.is_file() and not rhs.is_file():
                print(f"[Warning] Ignoring ({lhs}, {rhs}) - not files")

            pairs.append((lhs, rhs))

    print("\n--- --- --- --- --- --- --- --- --- ---\n")

    for lhs, rhs in pairs:
        print("Pair:")
        print(f"[!]: {lhs}")
        print(f"[!]: {rhs}\n")

        lhs = lhs.read_text()
        rhs = rhs.read_text()

        print("Metrics:")
        print(f"[?]: Damerau-Levenshtein - {damerau_levenshtein(lhs, rhs)}")
        print(f"[?]: Jaccard             - {jaccard(lhs, rhs)}")
        print(f"[?]: Jaro-Winkler        - {jaro_winkler(lhs, rhs)}")
        print(f"[?]: Jaro                - {jaro(lhs, rhs)}")
        print(f"[?]: Levenshtein         - {levenshtein(lhs, rhs)}")

        print("\n--- --- --- --- --- --- --- --- --- ---\n")


if __name__ == "__main__":
    main()
