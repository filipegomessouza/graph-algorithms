import random
from typing import Optional
from src.factories.factory import Factory
from src.structures.graph import Graph
from src.exceptions.invalid_factory_parameters_exception import InvalidFactoryParametersException

MIN_CYCLE_ATTEMPTS = 200
CYCLE_ATTEMPTS_PER_NODE = 50

class HierholzerFactory(Factory):
    def __init__(self, nodes_count: int, density: float, seed: Optional[int] = None):
        self._validate_parameters(nodes_count, density)

        self._nodes_count = nodes_count
        self._density = density
        self._rng = random.Random(seed)

    def create(self) -> Graph:
        graph = Graph()
        nodes = list(range(self._nodes_count))

        for node in nodes:
            graph.add_node(node)

        existing_edges = self._add_hamiltonian_cycle(graph, nodes)
        target_edges = self._target_edges()
        max_attempts = max(MIN_CYCLE_ATTEMPTS, self._nodes_count * CYCLE_ATTEMPTS_PER_NODE)

        failed_attempts = 0

        while graph.edges_count < target_edges and failed_attempts < max_attempts:
            remaining_budget = target_edges - graph.edges_count
            max_cycle_length = min(self._nodes_count, remaining_budget)

            if max_cycle_length < 3:
                break

            cycle_length = self._rng.randint(3, max_cycle_length)
            cycle = self._rng.sample(nodes, cycle_length)

            if self._can_add_cycle(cycle, existing_edges):
                self._add_cycle(graph, cycle, existing_edges)
                failed_attempts = 0
            else:
                failed_attempts += 1

        return graph

    def create_as_txt(self, file_path: str) -> None:
        graph = self.create()

        with open(file_path, 'w') as file:
            for from_node, to_node, _ in graph.get_edges():
                file.write(f"{from_node} {to_node}\n")

    def _target_edges(self) -> int:
        max_edges = self._nodes_count * (self._nodes_count - 1) // 2
        target_edges = round(self._density * max_edges)

        return max(target_edges, self._nodes_count)

    def _add_hamiltonian_cycle(self, graph: Graph, nodes: list):
        shuffled = self._rng.sample(nodes, self._nodes_count)
        existing_edges = set()

        for i in range(self._nodes_count):
            from_node = shuffled[i]
            to_node = shuffled[(i + 1) % self._nodes_count]

            graph.add_edge(from_node, to_node)
            existing_edges.add(self._canonical_edge(from_node, to_node))

        return existing_edges

    def _can_add_cycle(self, cycle: list, existing_edges: set) -> bool:
        for i in range(len(cycle)):
            from_node = cycle[i]
            to_node = cycle[(i + 1) % len(cycle)]

            if self._canonical_edge(from_node, to_node) in existing_edges:
                return False

        return True

    def _add_cycle(self, graph: Graph, cycle: list, existing_edges: set) -> None:
        for i in range(len(cycle)):
            from_node = cycle[i]
            to_node = cycle[(i + 1) % len(cycle)]

            graph.add_edge(from_node, to_node)
            existing_edges.add(self._canonical_edge(from_node, to_node))

    def _canonical_edge(self, from_node: int, to_node: int):
        return (min(from_node, to_node), max(from_node, to_node))

    def _validate_parameters(self, nodes_count: int, density: float) -> None:
        if nodes_count < 3:
            raise InvalidFactoryParametersException("nodes_count must be at least 3 to build an Eulerian cycle.")

        if not 0 <= density <= 1:
            raise InvalidFactoryParametersException("density must be between 0 and 1.")
