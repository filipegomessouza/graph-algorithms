from typing import List, Set, Tuple
from src.structures.graph import Graph
from src.algorithms.algorithm import Algorithm
from src.exceptions.invalid_graph_exception import InvalidGraphException
from copy import deepcopy

class HierholzerAlgorithm(Algorithm):
    def __init__(self, graph: Graph):
        super().__init__(graph)

    def run(self) -> List[int]:
        self._validate_graph()

        adjacency_list = deepcopy(self._graph.adjacency_list)
        current_path = [next(iter(adjacency_list))]
        visited_edges: Set[Tuple[int, int]] = set()

        circuit: List[int] = []

        while len(current_path) > 0:
            current_node = current_path[-1]

            if len(adjacency_list[current_node]) > 0:
                next_node = adjacency_list[current_node].pop()

                if (current_node, next_node) in visited_edges:
                    continue

                current_path.append(next_node)
                visited_edges.add((next_node, current_node))
            else:
                circuit.append(current_path.pop())

        return circuit

    def _validate_graph(self) -> None:
        if self._graph.is_empty():
            raise InvalidGraphException("The graph must not be empty.")

        if not self._graph.is_connected():
            raise InvalidGraphException("The graph must be connected.")

        for node in self._graph.adjacency_list.keys():
            if self._graph.get_degree(node) % 2 != 0:
                raise InvalidGraphException("All vertices in the graph must have an even degree.")
