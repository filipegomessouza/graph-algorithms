from typing import Any, List, Callable, Dict, Tuple
from abc import ABC, abstractmethod
from src.events.step_event import StepEvent
from src.structures.graph import Graph
from src.styles.node_style import NodeStyle
from src.styles.edge_style import EdgeStyle

StepCallback = Callable[[StepEvent], None]

class Algorithm(ABC):
    def __init__(self, graph: Graph):
        self._graph = graph
        self._listeners: List[StepCallback] = []
        self._step = 0

    @abstractmethod
    def run(self) -> Any:
        pass

    def add_listener(self, listener: StepCallback) -> 'Algorithm':
        self._listeners.append(listener)

        return self
    
    def _emit_step(self, description: str, node_styles: Dict[int, NodeStyle] = {}, edge_styles: Dict[Tuple[int, int], EdgeStyle] = {}) -> None:
        step_event = StepEvent(
            step=self._step,
            graph=self._graph,
            description=description,
            node_styles=node_styles,
            edge_styles=edge_styles
        )

        self._run_listeners(step_event)
        self._step += 1

    def _run_listeners(self, event: StepEvent) -> None:
        for listener in self._listeners:
            listener(event)
