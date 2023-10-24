def create_fill_levenshtein_matrix(size_lh_pp: int, size_rh_pp: int) -> list:
    matrix = [[0 for _ in range(size_rh_pp)] for _ in range(size_lh_pp)]
    for i in range(size_lh_pp):
        matrix[i][0] = i
    for i in range(size_rh_pp):
        matrix[0][i] = i
    return matrix


def damerau_levenshtein(lh: str, rh: str) -> int:
    size_lh_pp = len(lh) + 1
    size_rh_pp = len(rh) + 1

    table_dist = create_fill_levenshtein_matrix(size_lh_pp, size_rh_pp)

    for i in range(1, size_lh_pp):
        for j in range(1, size_rh_pp):
            value = min(table_dist[i - 1][j] + 1,
                        table_dist[i][j - 1] + 1,
                        table_dist[i - 1][j - 1] + (lh[i - 1] != rh[j - 1]))
            if i > 1 and j > 1 and lh[i - 1] == rh[j - 2] and lh[i - 2] == rh[j - 1]:
                value = min(value, table_dist[i - 2][j - 2] + (lh[i - 1] != rh[j - 1]))
            table_dist[i][j] = value

    return table_dist[size_lh_pp - 1][size_rh_pp - 1]
