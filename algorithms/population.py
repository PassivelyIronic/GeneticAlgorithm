import random
import numpy as np
from algorithms.individual import Individual
from algorithms.mutation import edge_mutation, single_point_mutation, two_point_mutation
from algorithms.selection import best_selection, roulette_selection, tournament_selection
from algorithms.crossover import single_point_crossover, two_point_crossover, uniform_crossover
from config import Config
from algorithms.chromosome import Chromosome

class Population:
    def __init__(self, config: Config):
        self.config = config
        self.size = config.population_size
        self.num_variables = config.num_variables
        self.bits_per_variable = config.precision
        self.precision = config.precision
        self.generation = 0

        self.individuals = [
            Individual(self.num_variables, self.bits_per_variable, self.precision)
            for _ in range(self.size)
        ]

    def evaluate_all(self, fitness_func, bounds):
        for individual in self.individuals:
            individual.evaluate(fitness_func, bounds)

    def select(self):
        method = self.config.selection_method

        if method == "tournament":
            return random.choice(tournament_selection(self.individuals, self.config.tournament_size))
        elif method == "best":
            return random.choice(best_selection(self.individuals, self.config.best_selection_amount))
        elif method == "roulette":
            return random.choice(roulette_selection(self.individuals, self.config.best_selection_amount))
        else:
            raise ValueError(f"Unknown selection method: {method}")

    def crossover(self, parent1, parent2):
        method = self.config.crossover_method
        offspring1 = Individual(self.num_variables, self.bits_per_variable, self.precision, False)
        offspring2 = Individual(self.num_variables, self.bits_per_variable, self.precision, False)

        for i in range(self.num_variables):
            if parent1.chromosomes[i] and parent2.chromosomes[i]:
                if method == "single_point":
                    child1_chrom, child2_chrom = single_point_crossover(
                        parent1.chromosomes[i], parent2.chromosomes[i]
                    )
                elif method == "two_point":
                    child1_chrom, child2_chrom = two_point_crossover(
                        parent1.chromosomes[i], parent2.chromosomes[i]
                    )
                elif method == "uniform":
                    child1_chrom, child2_chrom = uniform_crossover(
                        parent1.chromosomes[i], parent2.chromosomes[i]
                    )
                else:
                    raise ValueError(f"Unknown crossover method: {method}")
            
                if child1_chrom is not None and child2_chrom is not None:
                    offspring1.chromosomes[i] = child1_chrom
                    offspring2.chromosomes[i] = child2_chrom
                else:
                    offspring1.chromosomes[i] = Chromosome(parent1.chromosomes[i].get_chromosome_len(), False)
                    offspring1.chromosomes[i].set_chromosome(parent1.chromosomes[i].chromosome.copy())
                
                    offspring2.chromosomes[i] = Chromosome(parent2.chromosomes[i].get_chromosome_len(), False)
                    offspring2.chromosomes[i].set_chromosome(parent2.chromosomes[i].chromosome.copy())

        return offspring1, offspring2


    def mutate(self, individual: Individual):
        for chrom in individual.chromosomes:
            method = self.config.mutation_method
            if method == "edge":
                edge_mutation(chrom, self.config.mutation_probability)
            elif method == "single_point":
                single_point_mutation(chrom, self.config.mutation_probability)
            elif method == "two_point":
                two_point_mutation(chrom, self.config.mutation_probability)
            else:
                raise ValueError(f"Unknown mutation method: {method}")

    def evolve(self, fitness_func, bounds):
        self.evaluate_all(fitness_func, bounds)
        reverse_sort = self.config.optimization_type == "max"
        self.individuals.sort(key=lambda ind: ind.fitness, reverse=reverse_sort)

        new_population = []

        if self.config.elite_size > 0:
            new_population.extend(self.individuals[:self.config.elite_size])

        while len(new_population) < self.size:
            parent1 = self.select()
            parent2 = self.select()

            if random.random() < self.config.crossover_probability:
                offspring1, offspring2 = self.crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2

            self.mutate(offspring1)
            self.mutate(offspring2)

            new_population.append(offspring1)
            if len(new_population) < self.size:
                new_population.append(offspring2)

        self.individuals = new_population[:self.size]
        self.generation += 1

    def run(self, fitness_func, bounds):
        best_fitness_history = []
        avg_fitness_history = []

        for gen in range(self.config.epochs):
            self.evolve(fitness_func, bounds)

            best_fitness = min(ind.fitness for ind in self.individuals) if self.config.optimization_type == "min" else max(ind.fitness for ind in self.individuals)
            avg_fitness = sum(ind.fitness for ind in self.individuals) / self.size

            best_fitness_history.append(best_fitness)
            avg_fitness_history.append(avg_fitness)

            print(f"Pokolenie {gen+1}/{self.config.epochs}: Najlepsze przystosowanie = {best_fitness:.6f}, Średnie przystosowanie = {avg_fitness:.6f}")

        best_individual = min(self.individuals, key=lambda ind: ind.fitness) if self.config.optimization_type == "min" else max(self.individuals, key=lambda ind: ind.fitness)
        return best_individual, best_fitness_history, avg_fitness_history