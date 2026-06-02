from typing import List
from src.structures.graph import Graph
from src.algorithms.algorithm import Algorithm

class HierholzerAlgorithm(Algorithm):
    def __init__(self, graph: Graph):
        super().__init__(graph)

    def run(self) -> List[int]:
        pass
