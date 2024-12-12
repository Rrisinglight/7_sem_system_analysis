
def build_graph(edges_data: str):
    """
    В папку task2 загрузить файл с выполненным заданием (см. ниже); файл назвать task.py
    В файле task.py создать функцию main(var: str): str, которая в качестве аргумента
    принимает csv-строку, содержащую список ребер ориентированного графа-дерева.
    Функция возвращает список экстенсиональных длин (для i-ого элемента по j-тому отношению)
    для каждого узла по заданному набору отношений.
    Результат функция возвращает в виде csv-строки, в которой каждая строка соответствует узлу графа,
    а каждый элемент строки соответствует значению  для каждого вида отношений по соответствующему узлу. 
    - показывает количество узлов, с которыми узел i находится в отношении j
    """
    graph = {}
    parents = {}
    vertices = set()

    for edge in edges_data.strip().split('\n'):
        parent_node, child_node = map(int, edge.split(','))

        vertices.add(parent_node)
        vertices.add(child_node)

        graph.setdefault(parent_node, []).append(child_node)
        parents[child_node] = parent_node

    for v in vertices:
        graph.setdefault(v, [])

    return (graph, parents, vertices)


def dfs(graph, root, depth_level):

    count = 0

    def inner_dfs(vertex, level):
        nonlocal count
        if level == depth_level:
            count += 1
            return
        if level < depth_level:
            for child in graph[vertex]:
                inner_dfs(child, level + 1)

    inner_dfs(root, 0)
    return (count)


def count_matrix_metrics(graph, parents, node):

    child_count = dfs(graph, node, 1)
    parent_node = parents.get(node)
    direct_parent_count = 1 if parent_node else 0
    grandchild_count = dfs(graph, node, 2)

    uncle_count = 0
    if parent_node and parent_node in parents:
        grandparent_node = parents[parent_node]
        uncle_count = len(graph[grandparent_node]) - 1

    sibling_count = 0
    if parent_node:
        sibling_count = len(graph[parent_node]) - 1

    return ([child_count, direct_parent_count, grandchild_count, uncle_count, sibling_count])


def main(edges_data):

    graph, parents, vertices = build_graph(edges_data)
    sorted_vertices = sorted(vertices)

    result_lines = []
    for v in sorted_vertices:
        metrics = count_matrix_metrics(graph, parents, v)
        result_lines.append(' '.join(map(str, metrics)))

    return ('\n'.join(result_lines))


if __name__ == "__main__":

    test_data = "1,2\n1,3\n3,4\n3,5"

    print(main(test_data))
