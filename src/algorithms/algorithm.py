from typing import Any
from abc import ABC, abstractmethod
from src.structures.graph import Graph

class Algorithm(ABC):
    def __init__(self, graph: Graph):
        self._graph = graph


    @abstractmethod
    def run(self) -> Any:
        pass