from typing import Any
from abc import ABC, abstractmethod
from src.structures.graph import Graph

class Reader(ABC):
    @abstractmethod
    def read(self) -> Any:
        pass
