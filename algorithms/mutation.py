import random
from algorithms.chromosome import Chromosome

def edge_mutation(chromosome: Chromosome, probability: float = 1) -> None:
    if random.random() <= probability:
        chromosome.change_chromosome_bit(0)
        chromosome.change_chromosome_bit(chromosome.get_chromosome_len() - 1)


def single_point_mutation(chromosome: Chromosome, probability: float = 1) -> None:
    if random.random() <= probability:
        mutation_point = random.randint(0, chromosome.get_chromosome_len() - 1)
        chromosome.change_chromosome_bit(mutation_point)
        

def two_point_mutation(chromosome: Chromosome, probability: float = 1) -> None:
    if random.random() <= probability:
        points = random.sample(range(chromosome.get_chromosome_len()), 2)
        for point in points:
            chromosome.change_chromosome_bit(point)
