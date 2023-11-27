import jellyfish


def levenshtein(lhs: str, rhs: str) -> float:
    if not lhs and not rhs:
        return 1.0

    distance: int = jellyfish.levenshtein_distance(lhs, rhs)
    return 1.0 - distance / max(len(lhs), len(rhs))
