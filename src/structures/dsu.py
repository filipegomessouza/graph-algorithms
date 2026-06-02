from src.structures.graph import Graph

class DSU:
    def __init__(self, graph: Graph):
        self._parent = { node: node for node in graph.adjacency_list.keys() }
        self._rank = { node: 1 for node in graph.adjacency_list.keys() }

    def find(self, x: int) -> int:
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])

        return self._parent[x]

    def union(self, x: int, y: int) -> bool:
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return False

        if self._rank[x_root] < self._rank[y_root]:
            self._parent[x_root] = y_root
        elif self._rank[x_root] > self._rank[y_root]:
            self._parent[y_root] = x_root
        else:
            self._parent[y_root] = x_root
            self._rank[x_root] += 1

        return True
