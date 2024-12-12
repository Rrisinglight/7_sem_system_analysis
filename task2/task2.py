import csv
from io import StringIO
from collections import defaultdict
from typing import List, Dict


def parse_edges_to_graph(edge_csv: str) -> Dict[int, List[int]]:

    graph = defaultdict(list)
    reader = csv.reader(StringIO(edge_csv))

    for row in reader:
        if len(row) == 2:
            parent, child = map(int, row)
            graph[parent].append(child)

    return(graph)


def count_all_descendants(graph: Dict[int, List[int]], node: int) -> int:

    all_descendants = 0
    for child in graph[node]:
        all_descendants += 1
        all_descendants += count_all_descendants(graph, child)

    return(all_descendants)


def count_direct_ancestors(graph: Dict[int, List[int]], node: int) -> int:

    ancestor_count = 0
    for parent, children in graph.items():
        if node in children:
            ancestor_count += 1

    return(ancestor_count)


def count_all_ancestors(graph: Dict[int, List[int]], node: int) -> int:

    all_ancestors = 0
    for parent, children in graph.items():
        if node in children:
            all_ancestors += 1
            all_ancestors += count_all_ancestors(graph, parent)

    return(all_ancestors)


def count_near_nodes(graph: Dict[int, List[int]], node: int) -> int:

    near_count = 0
    for parent, children in graph.items():
        if node in children:
            near_count += len(graph[parent]) - 1

    return(near_count)


def calculate_node_relations(graph: Dict[int, List[int]], node: int) -> List[int]:

    row_1 = len(graph[node])  # Прямые потомки
    row_2 = count_direct_ancestors(graph, node)  # Прямые предки
    row_3 = count_all_descendants(graph, node) - row_1  # Все потомки
    row_4 = count_all_ancestors(graph, node) - row_2  # Все предки
    row_5 = count_near_nodes(graph, node)  # Соседи

    return([row_1, row_2, row_3, row_4, row_5])


def main(edge_csv: str) -> str:

    graph = parse_edges_to_graph(edge_csv)
    nodes = sorted(set(graph.keys()).union(*graph.values()))

    result = []
    for node in nodes:
        node_relations = calculate_node_relations(graph, node)
        result.append([node] + node_relations)

    return('\n'.join(','.join(map(str, row)) for row in result))


if __name__ == "__main__":
    test = "1,2\n1,3\n3,4\n3,5"

    print(main(test))
