import glob
import shutil
from pathlib import Path
from src.readers.hierholzer_reader import HierholzerReader
from src.readers.required_kruskal_reader import RequiredKruskalReader
from src.algorithms.hierholzer_algorithm import HierholzerAlgorithm
from src.algorithms.required_kruskal_algorithm import RequiredKruskalAlgorithm
from src.visualizers.graph_visualizer import GraphVisualizer

def run_hierholzer_instance(file_path: str) -> None:
    instance_name = Path(file_path).stem
    output_path = f"output/hierholzer/{instance_name}"
    shutil.rmtree(output_path, ignore_errors=True)

    graph = HierholzerReader(file_path).read()
    visualizer = GraphVisualizer(output_path)

    circuit = HierholzerAlgorithm(graph)\
        .add_listener(visualizer.on_step)\
        .run()

    print(f"[hierholzer/{instance_name}] Eulerian circuit:", circuit)

def run_required_kruskal_instance(file_path: str) -> None:
    instance_name = Path(file_path).stem
    output_path = f"output/required_kruskal/{instance_name}"
    shutil.rmtree(output_path, ignore_errors=True)

    graph, required_edges = RequiredKruskalReader(file_path).read()
    required_pairs = [(from_node, to_node) for from_node, to_node, _ in required_edges]
    visualizer = GraphVisualizer(output_path)

    tree, weight_sum = RequiredKruskalAlgorithm(graph, required_pairs)\
        .add_listener(visualizer.on_step)\
        .run()

    print(f"[required_kruskal/{instance_name}] MST weight:", weight_sum)

for file_path in sorted(glob.glob("instances/hierholzer_algorithm/*.txt")):
    run_hierholzer_instance(file_path)

for file_path in sorted(glob.glob("instances/required_kruskal_algorithm/*.txt")):
    run_required_kruskal_instance(file_path)
