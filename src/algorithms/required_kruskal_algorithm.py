from typing import List, Tuple, Set
from src.algorithms.algorithm import Algorithm
from src.exceptions.invalid_required_edges_exception import InvalidRequiredEdgesException
from src.exceptions.invalid_graph_exception import InvalidGraphException
from src.structures.dsu import DSU
from src.structures.graph import Graph
from src.styles.node_style import NodeStyle
from src.styles.edge_style import EdgeStyle
from src.enums.color import Color

class RequiredKruskalAlgorithm(Algorithm):
    def __init__(self, graph: Graph, required_edges: List[Tuple[int, int]]):
        super().__init__(graph)
        self._required_edges = required_edges
        self._dsu = DSU(graph)
        self._tree = Graph()

    def run(self) -> Tuple[Graph, int]:
        self._validated_graph()
        self._validate_required_edges()

        weight_sum = 0

        self._emit_tree('Start with empty tree')

        for u, v in self._required_edges:
            weight = self._graph.get_edge_weight(u, v)
            self._tree.add_edge(u, v, weight)
            weight_sum += weight

            if not self._dsu.union(u, v):
                raise InvalidRequiredEdgesException("The required edges create a cycle in the graph.")
            
        self._emit_tree('Add required edges')

        required_edges_set = set(self._required_edges)

        sorted_edges: List[Tuple[int, int, int]] = sorted(
            self._graph.get_edges(),
            key=lambda edge: edge[2],
        )

        for u, v, weight in sorted_edges:
            if self._tree.edges_count == self._graph.nodes_count - 1:
                break

            if (u, v) in required_edges_set or (v, u) in required_edges_set:
                continue

            self._emit_check_edge(u, v, weight)

            if not self._dsu.union(u, v):
                continue

            self._tree.add_edge(u, v, weight)
            weight_sum += weight

            self._emit_tree('Add edge')

        self._emit_tree('End: MST found')

        return self._tree, weight_sum

    def _validate_required_edges(self) -> None:
        for u, v in self._required_edges:
            if not self._graph.has_edge(u, v):
                raise InvalidRequiredEdgesException("There are edges in the required edges list that do not exist in the graph.")

    def _validated_graph(self) -> None:
        if self._graph.is_empty():
            raise InvalidGraphException("The graph must not be empty.")

        if not self._graph.is_connected():
            raise InvalidGraphException("The graph must be connected.")

    def _emit_check_edge(self, u: int, v: int, weight: int) -> None:
        node_styles = self._get_tree_node_style()
        edge_styles = self._get_tree_edge_style()

        node_styles[u] = NodeStyle(str(u), Color.RED, bold=True)
        node_styles[v] = NodeStyle(str(v), Color.RED, bold=True)
        edge_styles[(u, v)] = EdgeStyle(str(weight), Color.RED, bold=True)

        self._emit_step('Check edge', node_styles, edge_styles)

    def _emit_tree(self, description: str) -> None:
        node_styles = self._get_tree_node_style()
        edge_styles = self._get_tree_edge_style()

        self._emit_step(description, node_styles, edge_styles)

    def _get_tree_node_style(self) -> NodeStyle:
        def node_style(i: int) -> NodeStyle:
            node_is_in_tree = self._tree.has_node(i)
            color = Color.BLACK if node_is_in_tree else Color.GRAY

            return NodeStyle(str(i), color, bold=node_is_in_tree)
        
        return { i: node_style(i) for i in self._graph.get_nodes() }
    
    def _get_tree_edge_style(self) -> EdgeStyle:
        def edge_style(u: int, v: int, weight: int) -> EdgeStyle:
            edge_is_in_tree = self._tree.has_edge(u, v)
            color = Color.BLACK if edge_is_in_tree else Color.GRAY

            return EdgeStyle(str(weight), color, bold=edge_is_in_tree)
        
        return { (u, v): edge_style(u, v, weight) for u, v, weight in self._graph.get_edges() }
