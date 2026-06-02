from typing import List, Tuple
from src.algorithms.algorithm import Algorithm
from src.exceptions.invalid_required_edges_exception import InvalidRequiredEdgesException
from src.structures.dsu import DSU
from src.structures.graph import Graph

class RequiredKruskalAlgorithm(Algorithm):
    def __init__(self, graph: Graph, required_edges: List[Tuple[int, int]]):
        super().__init__(graph)
        self._required_edges = required_edges
        self._dsu = DSU(graph)

    def run(self) -> Tuple[Graph, int]:
        self._validated_graph()
        self._validate_required_edges()

        weight_sum = 0
        tree = Graph()

        for u, v in self._required_edges:
            weight = self._graph.get_edge_weight(u, v)
            tree.add_edge(u, v, weight)
            weight_sum += weight

            if not self._dsu.union(u, v):
                raise InvalidRequiredEdgesException("The required edges create a cycle in the graph.")

        required_edges_set = set(self._required_edges)

        sorted_edges: List[Tuple[int, int, int]] = sorted(
            self._graph.get_edges(),
            key=lambda edge: edge[2],
        )

        for u, v, weight in sorted_edges:
            if tree.edges_count == self._graph.nodes_count - 1:
                break

            if (u, v) in required_edges_set or (v, u) in required_edges_set or not self._dsu.union(u, v):
                continue

            tree.add_edge(u, v, weight)
            weight_sum += weight

        return tree, weight_sum

    def _validate_required_edges(self) -> None:
        for u, v in self._required_edges:
            if not self._graph.has_edge(u, v):
                raise InvalidRequiredEdgesException("There are edges in the required edges list that do not exist in the graph.")

    def _validated_graph(self) -> None:
        if not self._graph.is_connected():
            raise InvalidRequiredEdgesException("The graph must be connected.")
