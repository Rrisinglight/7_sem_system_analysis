def read_graph_connections(input_text):
    """
    Читает входные данные и создает простую структуру графа.
    
    :param input_text: Строка с ребрами графа
    :return: Словарь связей, где ключ - родительский узел, значение - список дочерних узлов
    """
    # Создаем пустой словарь для хранения связей
    graph_connections = {}
    
    # Преобразуем входной текст в строки
    graph_rows = input_text.strip().split('\n')
    
    # Обходим каждую строку
    for row in graph_rows:
        # Разделяем строку на родительский и дочерний узлы
        parent_node, child_node = map(int, row.split(','))
        
        # Если родительский узел еще не добавлен в словарь, создаем для него пустой список
        if parent_node not in graph_connections:
            graph_connections[parent_node] = []
        
        # Добавляем дочерний узел в список дочерних узлов родителя
        graph_connections[parent_node].append(child_node)
    
    return graph_connections

def find_direct_children(graph_connections, target_node):
    """
    Находит прямых потомков для указанного узла.
    
    :param graph_connections: Словарь связей графа
    :param target_node: Узел, для которого ищутся прямые потомки
    :return: Список прямых потомков
    """
    # Возвращаем список потомков, если узел есть в графе, иначе пустой список
    return graph_connections.get(target_node, [])

def find_direct_parents(graph_connections, target_node):
    """
    Находит прямых родителей для указанного узла.
    
    :param graph_connections: Словарь связей графа
    :param target_node: Узел, для которого ищутся прямые родители
    :return: Список прямых родителей
    """
    direct_parents = []
    
    # Обходим все узлы графа
    for parent, children in graph_connections.items():
        # Если target_node есть в списке детей, значит parent - родитель
        if target_node in children:
            direct_parents.append(parent)
    
    return direct_parents

def find_all_descendants(graph_connections, start_node):
    """
    Находит всех потомков узла, включая потомков потомков.
    
    :param graph_connections: Словарь связей графа
    :param start_node: Узел, для которого ищутся все потомки
    :return: Список всех потомков
    """
    # Список для хранения всех найденных потомков
    all_descendants = []
    
    # Список узлов, которые нужно обработать
    nodes_to_process = find_direct_children(graph_connections, start_node)
    
    # Пока есть узлы для обработки
    while nodes_to_process:
        # Берем первый узел из списка
        current_node = nodes_to_process[0]
        nodes_to_process = nodes_to_process[1:]
        
        # Добавляем текущий узел в список потомков
        all_descendants.append(current_node)
        
        # Находим детей текущего узла
        current_children = find_direct_children(graph_connections, current_node)
        
        # Добавляем детей в список узлов для обработки
        nodes_to_process.extend(current_children)
    
    return all_descendants

def find_all_ancestors(graph_connections, start_node):
    """
    Находит всех предков узла, включая предков предков.
    
    :param graph_connections: Словарь связей графа
    :param start_node: Узел, для которого ищутся все предки
    :return: Список всех предков
    """
    # Список для хранения всех найденных предков
    all_ancestors = []
    
    # Список узлов, которые нужно обработать
    nodes_to_process = find_direct_parents(graph_connections, start_node)
    
    # Пока есть узлы для обработки
    while nodes_to_process:
        # Берем первый узел из списка
        current_node = nodes_to_process[0]
        nodes_to_process = nodes_to_process[1:]
        
        # Добавляем текущий узел в список предков
        all_ancestors.append(current_node)
        
        # Находим родителей текущего узла
        current_parents = find_direct_parents(graph_connections, current_node)
        
        # Добавляем родителей в список узлов для обработки
        nodes_to_process.extend(current_parents)
    
    return all_ancestors

def analyze_node_relations(graph_connections):
    """
    Анализирует отношения для каждого узла в графе.
    
    :param graph_connections: Словарь связей графа
    :return: Список результатов для каждого узла
    """
    # Находим все уникальные узлы в графе
    all_nodes = set(list(graph_connections.keys()) + 
                    [node for children in graph_connections.values() for node in children])
    
    # Список для хранения результатов
    node_relations = []
    
    # Анализируем отношения для каждого узла
    for target_node in sorted(all_nodes):
        # 1. Количество прямых потомков
        direct_children_count = len(find_direct_children(graph_connections, target_node))
        
        # 2. Количество прямых родителей
        direct_parents_count = len(find_direct_parents(graph_connections, target_node))
        
        # 3. Количество всех потомков (кроме прямых детей)
        all_descendants = find_all_descendants(graph_connections, target_node)
        indirect_descendants_count = len(all_descendants) - direct_children_count
        
        # 4. Количество всех предков (кроме прямых родителей)
        all_ancestors = find_all_ancestors(graph_connections, target_node)
        indirect_ancestors_count = len(all_ancestors) - direct_parents_count
        
        # 5. Сумма количества потомков у родителей минус 1
        indirect_relations_count = sum(
            len(find_direct_children(graph_connections, parent)) - 1
            for parent in find_direct_parents(graph_connections, target_node)
        )
        
        # Сохраняем результаты
        node_relations.append([
            target_node, 
            direct_children_count, 
            direct_parents_count, 
            indirect_descendants_count, 
            indirect_ancestors_count, 
            indirect_relations_count
        ])
    
    return node_relations

def main(input_text):
    """
    Основная функция для анализа графа.
    
    :param input_text: Входной текст с ребрами графа
    :return: Строка с результатами анализа
    """
    # Читаем граф из входных данных
    graph_connections = read_graph_connections(input_text)
    
    # Анализируем отношения узлов
    node_relations = analyze_node_relations(graph_connections)
    
    # Преобразуем результаты в строку
    output_rows = []
    for row in node_relations:
        output_rows.append(','.join(map(str, row)))
    
    return '\n'.join(output_rows)

# Пример использования
if __name__ == "__main__":
    example_graph_text = """1,2
1,3
3,4
3,5"""
    
    result = main(example_graph_text)
    print(result)