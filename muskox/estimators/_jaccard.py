def jaccard(lhs: str, rhs: str) -> float:
    if not isinstance(lhs, str):
        raise TypeError("The argument 'lhs' must be 'str'")

    if not isinstance(rhs, str):
        raise TypeError("The argument 'rhs' must be 'str'")

    if not lhs and not rhs:
        return 1.0

    lh_set = set(lhs.split())
    rh_set = set(rhs.split())

    len_intersect_words = len(lh_set.intersection(rh_set))
    len_union_words = len(lh_set.union(rh_set))

    return len_intersect_words / len_union_words
