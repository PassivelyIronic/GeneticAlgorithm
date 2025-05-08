from algorithms.chromosome import Chromosome
from algorithms.config import config
import random
from algorithms.mutation import single_point_mutation, two_point_mutation, edge_mutation

class Individual:
    def __init__(self, num_variables=2, precision=10, bits_per_variable=None, random_init=True):
        self.num_variables = num_variables
        self.precision = precision
        self.bits_per_variable = bits_per_variable if bits_per_variable is not None else precision
        self.chromosomes = [Chromosome(num_bits=self.bits_per_variable, random_init=random_init) for _ in range(self.num_variables)]
        self.fitness = float('inf')
        self.chromosome_values = []

    def evaluate(self, fitness_func=None, bounds=None):
        self.chromosome_values = []

        range_start = bounds[0] if bounds else config.range_start
        range_end = bounds[1] if bounds else config.range_end
    
        for chromosome in self.chromosomes:
            value = chromosome.decode(a=range_start, b=range_end)
            if value is not None:
                self.chromosome_values.append(value)
            else:
                print(f"Warning: Chromosome decode failed.")
                self.chromosome_values.append(0)

        if fitness_func:
            self.fitness = fitness_func(self)
        else:
            from algorithms.fitness import evaluate_fitness
            self.fitness = evaluate_fitness(self)
    
        return self.fitness


    def apply_mutation(self, mutation_rate=0.3, method="single_point"):
        for chromosome in self.chromosomes:
            if method == "single_point":
                single_point_mutation(chromosome, probability=mutation_rate)
            elif method == "two_point":
                two_point_mutation(chromosome, probability=mutation_rate)
            elif method == "edge":
                edge_mutation(chromosome, probability=mutation_rate)
            else:
                print(f"Ostrzeżenie: Nieznana metoda mutacji: {method}")