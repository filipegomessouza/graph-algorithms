from typing import List
from src.seeders.seeder import Seeder
from src.seeders.hierholzer_seeder import HierholzerSeeder
from src.seeders.required_kruskal_seeder import RequiredKruskalSeeder

seeders: List[Seeder] = [
    HierholzerSeeder(),
    RequiredKruskalSeeder(),
]

for seeder in seeders:
    seeder.run()
