from typing import List, Tuple
from src.structures.graph import Graph
from src.readers.reader import Reader

Edge = Tuple[int, int, int]
EdgeList = List[Edge]

class RequiredKruskalReader(Reader):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def read(self) -> Tuple[Graph, EdgeList]:
        graph = Graph()
        required_edges: EdgeList = []

        with open(self._file_path, 'r') as file:
            for line in file:
                from_node, to_node, weight, is_required = self._parse_line(line)
                graph.add_edge(from_node, to_node, weight)

                if is_required:
                    required_edges.append((from_node, to_node, weight))

        return graph, required_edges

    def _parse_line(self, line: str) -> Tuple[int, int, int, bool]:
        from_node, to_node, weight, is_required = map(int, line.strip().split())

        return from_node, to_node, weight, bool(is_required)
