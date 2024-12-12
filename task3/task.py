import sys
import csv
from math import log2


def parse_edges_to_graph(edge_csv: str):

    graph = []
    for line in edge_csv.strip().splitlines():
        values = list(map(int, line.split(",")))
        graph.append(values)

    return(graph)


def calc_entropy(graph):

    n = len(graph)
    ent = 0
    for row in graph:
        for l in row:
            if l > 0:
                p = l / (n - 1)
                ent += p * log2(p)
    return(round(-ent, 1))


def main(edge_csv: str):

    graph = parse_edges_to_graph(edge_csv)
    return(calc_entropy(graph))


def main_from_file(filepath: str):

    with open(filepath, "r") as file:
        edge_csv = file.read()

    return(main(edge_csv))


if __name__ == "__main__":

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "C:/Users/sirin/Documents/7_sem_system_analysis/task3/task3.csv"

    res = main_from_file(filepath)
    
    print(res)
