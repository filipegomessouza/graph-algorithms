from src.structures.graph import Graph
from src.algorithms.required_kruskal_algorithm import RequiredKruskalAlgorithm
from src.algorithms.hierholzer_algorithm import HierholzerAlgorithm
from src.visualizers.graph_visualizer import GraphVisualizer

required_kruskal_graph_visualizer = GraphVisualizer('output/required_kruskal')

toy_graph = Graph()\
    .add_edge(0, 1, 4)\
    .add_edge(0, 2, 1)\
    .add_edge(1, 2, 2)\
    .add_edge(1, 3, 5)\
    .add_edge(2, 3, 8)\

tree, weight_sum = RequiredKruskalAlgorithm(toy_graph, [(1, 0), (0, 2)])\
    .add_listener(required_kruskal_graph_visualizer.on_step)\
    .run()

print("MST weight:", weight_sum)

hierholzer_graph_visualizer = GraphVisualizer('output/hierholzer')

toy_graph_2 = Graph()\
    .add_edge(1, 2)\
    .add_edge(1, 3)\
    .add_edge(2, 3)\
    .add_edge(3, 4)\
    .add_edge(3, 5)\
    .add_edge(4, 5)\

circuit = HierholzerAlgorithm(toy_graph_2)\
    .add_listener(hierholzer_graph_visualizer.on_step)\
    .run()

print("Eulerian circuit:", circuit)
