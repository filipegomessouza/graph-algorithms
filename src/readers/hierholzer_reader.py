from src.structures.graph import Graph
from src.readers.reader import Reader

class HierholzerReader(Reader):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def read(self) -> Graph:
        graph = Graph()

        with open(self._file_path, 'r') as file:
            for line in file:
                from_node, to_node = map(int, line.strip().split())
                graph.add_edge(from_node, to_node)

        return graph
