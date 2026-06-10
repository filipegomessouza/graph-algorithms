from pathlib import Path
from src.events.step_event import StepEvent
import graphviz

class GraphVisualizer:
    def __init__(self, output_path: str):
        self._output_path = Path(output_path)
        self._output_path.mkdir(parents=True, exist_ok=True)

    def on_step(self, step_event: StepEvent) -> None:
        visualization_graph = self._build_visualization_graph(step_event)
        filename = self._output_path / f'step_{step_event.step}'
        visualization_graph.render(filename=filename, format='png', cleanup=True)

    def _build_visualization_graph(self, step_event: StepEvent) -> graphviz.Graph:
        pass
