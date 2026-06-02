from src.structures.graph import Graph
from src.algorithms.required_kruskal_algorithm import RequiredKruskalAlgorithm
from src.algorithms.hierholzer_algorithm import HierholzerAlgorithm

toy_graph = Graph()\
    .add_edge(0, 1, 4)\
    .add_edge(0, 2, 1)\
    .add_edge(1, 2, 2)\
    .add_edge(1, 3, 5)\
    .add_edge(2, 3, 8)\

required_kruskal_algorithm = RequiredKruskalAlgorithm(toy_graph, [(1, 0), (0, 2)])

tree, weight_sum = required_kruskal_algorithm.run()

print("MST weight:", weight_sum)
print(tree)
