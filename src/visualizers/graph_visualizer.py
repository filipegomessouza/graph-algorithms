from pathlib import Path
from src.enums.color import Color
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
        visualization_graph = graphviz.Graph(
            graph_attr={
                "rankdir": "LR",
                "label": step_event.description,
                "fontsize": "12",
            },
            node_attr={
                "shape": "circle",
            },
        )

        for node in step_event.graph.get_nodes():
            node_style = step_event.node_styles.get(node, None)
            color = node_style.color.value if node_style is not None else Color.BLACK.value

            visualization_graph.node(
                str(node),
                color=color,
                fontcolor=color,
                penwidth="2.5" if node_style is not None and node_style.bold else "1.0",
                style="filled" if node_style is not None and node_style.fill else "solid",
            )

        for u, v, weight in step_event.graph.get_edges():
            u, v = min(u, v), max(u, v)
            edge_styles = step_event.edge_styles.get((u, v), step_event.edge_styles.get((v, u), None))
            color = edge_styles.color.value if edge_styles is not None else Color.BLACK.value

            visualization_graph.edge(
                 str(u),
                 str(v),
                 label=str(weight),
                 color=color,
                 fontcolor=color,
                 penwidth="2.5" if edge_styles is not None and edge_styles.bold else "1.0",
            ),

        return visualization_graph
