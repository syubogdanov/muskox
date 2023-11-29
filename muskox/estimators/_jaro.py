import jellyfish


def jaro(lhs: str, rhs: str) -> float:
    if not isinstance(lhs, str):
        raise TypeError("The argument 'lhs' must be 'str'")

    if not isinstance(rhs, str):
        raise TypeError("The argument 'rhs' must be 'str'")

    if not lhs and not rhs:
        return 1.0

    return jellyfish.jaro_similarity(lhs, rhs)
