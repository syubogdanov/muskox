import jellyfish


def damerau_levenshtein(lhs: str, rhs: str) -> float:
    if not isinstance(lhs, str):
        raise TypeError("The argument 'lhs' must be 'str'")

    if not isinstance(rhs, str):
        raise TypeError("The argument 'rhs' must be 'str'")

    if not lhs and not rhs:
        return 1.0

    distance: int = jellyfish.damerau_levenshtein_distance(lhs, rhs)
    return 1.0 - distance / max(len(lhs), len(rhs))
