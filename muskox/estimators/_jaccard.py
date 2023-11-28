def jaccard(lhs: str, rhs: str) -> float:
    if not isinstance(lhs, str):
        raise TypeError("The argument 'lhs' must be 'str'")

    if not isinstance(rhs, str):
        raise TypeError("The argument 'rhs' must be 'str'")

    if not lhs or not rhs:
        return 1.0

    lh_set = set(lhs.split())
    rh_set = set(rhs.split())

    len_intersect_words = len(lh_set.intersection(rh_set))
    len_union_words = len(lh_set.union(rh_set))

    if len_union_words == 0:
        return 0.0

    return len_intersect_words / len_union_words
