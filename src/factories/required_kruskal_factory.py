import random
from typing import List, Tuple, Optional
from src.factories.factory import Factory
from src.structures.graph import Graph
from src.structures.dsu import DSU
from src.exceptions.invalid_factory_parameters_exception import InvalidFactoryParametersException

Edge = Tuple[int, int, int]
EdgesList = List[Edge]

MAX_EDGE_ATTEMPTS = 200

class RequiredKruskalFactory(Factory):
    def __init__(
        self,
        nodes_count: int,
        density: float,
        required_edges_ratio: float,
        min_weight: int = 1,
        max_weight: int = 10,
        seed: Optional[int] = None,
    ):
        self._validate_parameters(nodes_count, density, required_edges_ratio, min_weight, max_weight)

        self._nodes_count = nodes_count
        self._density = density
        self._required_edges_ratio = required_edges_ratio
        self._min_weight = min_weight
        self._max_weight = max_weight
        self._rng = random.Random(seed)

    def create(self) -> Tuple[Graph, EdgesList]:
        graph = Graph()
        nodes = list(range(self._nodes_count))

        for node in nodes:
            graph.add_node(node)

        existing_edges = self._add_random_spanning_tree(graph, nodes)
        self._fill_random_edges(graph, nodes, existing_edges)
        required_edges = self._select_required_edges(graph)

        return graph, required_edges

    def create_as_txt(self, file_path: str) -> None:
        graph, required_edges = self.create()
        required_set = {self._canonical_edge(u, v) for u, v, _ in required_edges}

        with open(file_path, 'w') as file:
            for from_node, to_node, weight in graph.get_edges():
                is_required = 1 if self._canonical_edge(from_node, to_node) in required_set else 0
                file.write(f"{from_node} {to_node} {weight} {is_required}\n")

    def _add_random_spanning_tree(self, graph: Graph, nodes: list) -> set:
        shuffled = self._rng.sample(nodes, self._nodes_count)
        existing_edges = set()

        for i in range(1, self._nodes_count):
            child = shuffled[i]
            parent = self._rng.choice(shuffled[:i])
            weight = self._rng.randint(self._min_weight, self._max_weight)

            graph.add_edge(child, parent, weight)
            existing_edges.add(self._canonical_edge(child, parent))

        return existing_edges

    def _fill_random_edges(self, graph: Graph, nodes: list, existing_edges: set) -> None:
        max_edges = self._nodes_count * (self._nodes_count - 1) // 2
        target_edges = min(max_edges, max(self._nodes_count - 1, round(self._density * max_edges)))

        failed_attempts = 0

        while graph.edges_count < target_edges and failed_attempts < MAX_EDGE_ATTEMPTS:
            from_node, to_node = self._rng.sample(nodes, 2)
            edge = self._canonical_edge(from_node, to_node)

            if edge in existing_edges:
                failed_attempts += 1
                continue

            weight = self._rng.randint(self._min_weight, self._max_weight)
            graph.add_edge(from_node, to_node, weight)
            existing_edges.add(edge)
            failed_attempts = 0

    def _select_required_edges(self, graph: Graph) -> EdgesList:
        max_forest_size = self._nodes_count - 1
        required_count = round(self._required_edges_ratio * max_forest_size)

        shuffled_edges = graph.get_edges()
        self._rng.shuffle(shuffled_edges)

        dsu = DSU(graph)
        required_edges: EdgesList = []

        for from_node, to_node, weight in shuffled_edges:
            if len(required_edges) >= required_count:
                break

            if dsu.union(from_node, to_node):
                required_edges.append((from_node, to_node, weight))

        return required_edges

    def _canonical_edge(self, from_node: int, to_node: int):
        return (min(from_node, to_node), max(from_node, to_node))

    def _validate_parameters(
        self,
        nodes_count: int,
        density: float,
        required_edges_ratio: float,
        min_weight: int,
        max_weight: int,
    ) -> None:
        if nodes_count < 2:
            raise InvalidFactoryParametersException("nodes_count must be at least 2.")

        if not 0 <= density <= 1:
            raise InvalidFactoryParametersException("density must be between 0 and 1.")

        if not 0 <= required_edges_ratio <= 1:
            raise InvalidFactoryParametersException("required_edges_ratio must be between 0 and 1.")

        if max_weight < min_weight:
            raise InvalidFactoryParametersException("weight range must satisfy min_weight <= max_weight.")
