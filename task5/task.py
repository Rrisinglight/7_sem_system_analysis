import json
from collections import defaultdict

json_a = "[1,[2,3],4,[5,6,7],8,9,10]"
json_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"

def construct_dominance_matrix(ranking):
    element_rank = defaultdict(int)
    reversed_ranking = reversed(ranking)

    for rank_level, group in enumerate(reversed_ranking, start=1):
        if isinstance(group, list):
            for element in group:
                element_rank[element] = rank_level
        else:
            element_rank[group] = rank_level

    elements = sorted(element_rank.keys())
    matrix_size = len(elements)

    dominance_matrix = [[0] * matrix_size for _ in range(matrix_size)]
    for i in range(matrix_size):
        for j in range(matrix_size):
            if element_rank[i+1] >= element_rank[j+1]:
                dominance_matrix[i][j] = 1

    return dominance_matrix


def main(json_ranking_a, json_ranking_b):
    ranking_a = json.loads(json_ranking_a)
    ranking_b = json.loads(json_ranking_b)

    dominance_a = construct_dominance_matrix(ranking_a)
    dominance_b = construct_dominance_matrix(ranking_b)

    n = len(dominance_a)

    agr_m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            agr_m[i][j] = dominance_a[i][j] * dominance_b[i][j]

    trans_agr = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            trans_agr[i][j] = agr_m[j][i]

    pairs_conflict = []
    for i in range(n):
        for j in range(i + 1, n):
            if agr_m[i][j] + trans_agr[i][j] == 0:
                pairs_conflict.append([i + 1, j + 1])

    return (json.dumps(pairs_conflict))


if __name__ == "__main__":
    result = main(json_a, json_b)
    print(result)