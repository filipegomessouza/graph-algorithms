from src.factories.hierholzer_factory import HierholzerFactory
from src.seeders.seeder import Seeder

class HierholzerSeeder(Seeder):
    def run(self) -> None:
        instances = [
            ("instances/hierholzer_algorithm/small.txt", 6, 0.3, 1),
            ("instances/hierholzer_algorithm/medium.txt", 12, 0.5, 2),
            ("instances/hierholzer_algorithm/large.txt", 20, 0.7, 3),
        ]

        for file_path, nodes_count, density, seed in instances:
            HierholzerFactory(nodes_count, density, seed=seed).create_as_txt(file_path)
            print(f"Generated {file_path}")
