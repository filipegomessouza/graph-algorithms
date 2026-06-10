from typing import Dict, Tuple
from src.styles.node_style import NodeStyle
from src.styles.edge_style import EdgeStyle
from dataclasses import dataclass
from src.structures.graph import Graph

@dataclass
class StepEvent:
    step: int
    graph: Graph
    description: str
    node_styles: Dict[int, NodeStyle]
    edge_styles: Dict[Tuple[int, int], EdgeStyle]
