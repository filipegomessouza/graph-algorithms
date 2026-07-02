from src.factories.hierholzer_factory import HierholzerFactory
from src.factories.required_kruskal_factory import RequiredKruskalFactory

hierholzer_instances = [
    ("instances/hierholzer_algorithm/small.txt", 6, 0.3, 1),
    ("instances/hierholzer_algorithm/medium.txt", 12, 0.5, 2),
    ("instances/hierholzer_algorithm/large.txt", 20, 0.7, 3),
]

for file_path, nodes_count, density, seed in hierholzer_instances:
    HierholzerFactory(nodes_count, density, seed=seed).create_as_txt(file_path)
    print(f"Generated {file_path}")

required_kruskal_instances = [
    ("instances/required_kruskal_algorithm/small.txt", 6, 0.4, 0.5, 1),
    ("instances/required_kruskal_algorithm/medium.txt", 12, 0.5, 0.4, 2),
    ("instances/required_kruskal_algorithm/large.txt", 20, 0.6, 0.3, 3),
]

for file_path, nodes_count, density, required_edges_ratio, seed in required_kruskal_instances:
    RequiredKruskalFactory(nodes_count, density, required_edges_ratio, seed=seed).create_as_txt(file_path)
    print(f"Generated {file_path}")
