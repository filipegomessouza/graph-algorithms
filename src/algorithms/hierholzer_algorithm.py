from typing import List, Set, Tuple, Dict
from src.structures.graph import Graph
from src.algorithms.algorithm import Algorithm
from src.exceptions.invalid_graph_exception import InvalidGraphException
from src.styles.node_style import NodeStyle
from src.styles.edge_style import EdgeStyle
from src.enums.color import Color
from copy import deepcopy

class HierholzerAlgorithm(Algorithm):
    def __init__(self, graph: Graph):
        super().__init__(graph)

    def run(self) -> List[int]:
        self._validate_graph()

        adjacency_list = deepcopy(self._graph.adjacency_list)
        start_node = next(iter(adjacency_list))
        current_path = [start_node]
        visited_edges: Set[Tuple[int, int]] = set()
        circuit: List[int] = []

        self._emit_start(start_node)

        while len(current_path) > 0:
            current_node = current_path[-1]

            if len(adjacency_list[current_node]) > 0:
                next_node = adjacency_list[current_node].pop()

                if (current_node, next_node) in visited_edges:
                    continue

                current_path.append(next_node)
                visited_edges.add((next_node, current_node))

                self._emit_traverse_edge(current_node, next_node, current_path, circuit, visited_edges)
            else:
                node = current_path.pop()
                circuit.append(node)

                self._emit_backtrack(node, current_path, circuit, visited_edges)

        circuit.reverse()
        self._emit_final_circuit(circuit)

        return circuit

    def _validate_graph(self) -> None:
        if self._graph.is_empty():
            raise InvalidGraphException("The graph must not be empty.")

        if not self._graph.is_connected():
            raise InvalidGraphException("The graph must be connected.")

        for node in self._graph.adjacency_list.keys():
            if self._graph.get_degree(node) % 2 != 0:
                raise InvalidGraphException("All vertices in the graph must have an even degree.")

    def _emit_start(self, start_node: int) -> None:
        def node_style(node: int) -> NodeStyle:
            is_start_node = node == start_node
            color = Color.RED if is_start_node else Color.GRAY

            return NodeStyle(str(node), color, bold=is_start_node)

        node_styles = { node: node_style(node) for node in self._graph.get_nodes() }
        edge_styles = { (u, v): EdgeStyle() for u, v, weight in self._graph.get_edges() }

        self._emit_step(f'Initialize: start at node {start_node}', node_styles, edge_styles)

    def _emit_traverse_edge(self, current_node: int, next_node: int, current_path: List[int], circuit: List[int], visited_edges: Set[Tuple[int, int]]) -> None:
        node_styles = self._build_node_styles(current_node, next_node, current_path, circuit)
        edge_styles = self._build_edge_styles(current_node, next_node, visited_edges, circuit)

        self._emit_step(f'Traverse edge ({current_node} → {next_node})', node_styles, edge_styles)

    def _emit_backtrack(self, node: int, current_path: List[int], circuit: List[int], visited_edges: Set[Tuple[int, int]]) -> None:
        node_styles = self._build_node_styles(None, None, current_path, circuit)
        edge_styles = self._build_edge_styles(None, None, visited_edges, circuit)

        self._emit_step(f'Backtrack: node {node} added to circuit', node_styles, edge_styles)

    def _emit_final_circuit(self, circuit: List[int]) -> None:
        circuit_edges = self._get_circuit_edges(circuit)

        node_styles = { node: NodeStyle(str(node), Color.GREEN, bold=True) for node in self._graph.get_nodes() }

        edge_styles = {
            (u, v): EdgeStyle(color=Color.GREEN if (min(u, v), max(u, v)) in circuit_edges else Color.GRAY, bold=(min(u, v), max(u, v)) in circuit_edges)
            for u, v, weight in self._graph.get_edges()
        }

        self._emit_step(f'Eulerian Circuit: {" → ".join(str(n) for n in circuit)}', node_styles, edge_styles)

    def _build_node_styles(self, active_node1: int|None, active_node2: int|None, current_path: List[int], circuit: List[int]) -> Dict[int, NodeStyle]:
        current_path_set: Set[int] = set(current_path)
        circuit_set: Set[int] = set(circuit)
        styles: Dict[int, NodeStyle] = {}

        for node in self._graph.get_nodes():
            if node in circuit_set:
                styles[node] = NodeStyle(str(node), Color.GREEN, bold=True)
            elif node == active_node1 or node == active_node2:
                styles[node] = NodeStyle(str(node), Color.RED, bold=True)
            elif node in current_path_set:
                styles[node] = NodeStyle(str(node), Color.BLUE, bold=True)
            else:
                styles[node] = NodeStyle(str(node), Color.GRAY)

        return styles

    def _build_edge_styles(self, active_u, active_v, visited_edges: Set[Tuple[int, int]], circuit: List[int]) -> Dict[Tuple[int, int], EdgeStyle]:
        circuit_edges = self._get_circuit_edges(circuit)
        styles: Dict[Tuple[int, int], EdgeStyle] = {}

        for u, v, weight in self._graph.get_edges():
            key = (min(u, v), max(u, v))
            is_circuit = key in circuit_edges

            is_active = (
                active_u is not None and active_v is not None and
                ((u == active_u and v == active_v) or (u == active_v and v == active_u))
            )

            is_visited = (u, v) in visited_edges or (v, u) in visited_edges

            if is_circuit:
                styles[(u, v)] = EdgeStyle(color=Color.GREEN, bold=True)
            elif is_active:
                styles[(u, v)] = EdgeStyle(color=Color.RED, bold=True)
            elif is_visited:
                styles[(u, v)] = EdgeStyle(color=Color.BLUE, bold=True)
            else:
                styles[(u, v)] = EdgeStyle(color=Color.GRAY)

        return styles

    def _get_circuit_edges(self, circuit: List[int]) -> Set[Tuple[int, int]]:
        edges: Set[Tuple[int, int]] = set()

        for i in range(len(circuit) - 1):
            u, v = circuit[i], circuit[i + 1]
            edges.add((min(u, v), max(u, v)))

        return edges
