from typing import List, Dict, Tuple, Set

class Graph:
    def __init__(self):
        self._adjacency_list: Dict[int, List[int]] = {}
        self._weights: Dict[Tuple[int, int], int] = {}
        self._nodes_count = 0
        self._edges_count = 0

    @property
    def nodes_count(self) -> int:
        return self._nodes_count

    @property
    def edges_count(self) -> int:
        return self._edges_count

    @property
    def adjacency_list(self) -> Dict[int, List[int]]:
        return self._adjacency_list

    def add_edge(self, from_node: int, to_node: int, weight: int = 1) -> "Graph":
        self.add_node(from_node)
        self.add_node(to_node)

        self._adjacency_list[from_node].append(to_node)
        self._adjacency_list[to_node].append(from_node)

        self._weights[(from_node, to_node)] = weight
        self._weights[(to_node, from_node)] = weight

        self._edges_count += 1

        return self

    def add_node(self, node: int) -> "Graph":
        if node not in self._adjacency_list:
            self._adjacency_list[node] = []
            self._nodes_count += 1

        return self

    def has_edge(self, from_node: int, to_node: int) -> bool:
        return to_node in self._adjacency_list.get(from_node, [])

    def get_edge_weight(self, from_node: int, to_node: int) -> int:
        return self._weights.get((from_node, to_node), 0)

    def get_degree(self, node: int) -> int:
        return len(self._adjacency_list.get(node, []))

    def get_edges(self) -> List[Tuple[int, int, int]]:
        edges: List[Tuple[int, int, int]] = []

        for (from_node, to_node), weight in self._weights.items():
            if from_node < to_node:
                edges.append((from_node, to_node, weight))

        return edges

    def is_empty(self) -> bool:
        return self._nodes_count == 0

    def is_connected(self) -> bool:
        if self.is_empty():
            return True

        visited: Set[int] = set()
        self._dfs(next(iter(self._adjacency_list)), visited)

        return len(visited) == self._nodes_count

    def _dfs(self, node: int, visited: Set[int]) -> None:
        visited.add(node)

        for neighbor in self._adjacency_list[node]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)

    def __str__(self) -> str:
        to_str = f"Graph(nodes_count={self._nodes_count}, edges_count={self._edges_count})\n"

        for node, neighbors in self._adjacency_list.items():
            to_str += f"\n  {node}: {neighbors}"

        return to_str
