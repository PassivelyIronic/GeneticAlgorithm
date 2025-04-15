from algorithms.config import config
from algorithms.selection import best_selection, roulette_selection, tournament_selection
from algorithms.crossover import single_point_crossover, two_point_crossover, uniform_crossover
from algorithms.mutation import single_point_mutation, two_point_mutation, edge_mutation
from algorithms.inversion import inversion
from algorithms.fitness import evaluate_fitness
from algorithms.chromosome import Chromosome
from algorithms.individual import Individual
from apps.plotter import Plotter
import random
import numpy as np
import time

def run_genetic_algorithm():
    population_size = config.population_size
    num_epochs = config.epochs
    crossover_rate = config.crossover_probability
    mutation_rate = config.mutation_probability
    inversion_rate = config.inversion_probability
    elitism_count = config.best_selection_amount
    selection_method = config.selection_method
    crossover_method = config.crossover_method
    num_variables = config.num_variables
    precision = config.precision
    
    bounds = (config.range_start, config.range_end)

    plotter = Plotter()

    start_time = time.time()

    population = [Individual(num_variables=num_variables, precision=precision) for _ in range(population_size)]
    
    for ind in population:
        ind.evaluate(evaluate_fitness, bounds)

    if config.optimization_type == "max":
        best_individual = max(population, key=lambda ind: ind.fitness)
        optimization_func = max
    else:
        best_individual = min(population, key=lambda ind: ind.fitness)
        optimization_func = min

    avg_fitness = sum(ind.fitness for ind in population) / len(population)
    
    plotter.update_history(best_individual.fitness, avg_fitness)
    
    print(f"Epoka 0, najlepsze przystosowanie: {best_individual.fitness}")

    for generation in range(1, num_epochs + 1):

        if selection_method == "best":
            selected = best_selection(population, config.best_selection_amount)
        elif selection_method == "roulette":
            selected = roulette_selection(population, population_size)
        else:
            selected = tournament_selection(population, tournament_size=config.tournament_size)

        if config.optimization_type == "max":
            elites = sorted(population, key=lambda ind: ind.fitness, reverse=True)[:elitism_count]
        else:
            elites = sorted(population, key=lambda ind: ind.fitness)[:elitism_count]

        new_population = []

        while len(new_population) < population_size - elitism_count:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)

            if random.random() < crossover_rate:
                child1 = Individual(num_variables=num_variables, precision=precision, random_init=False)
                child2 = Individual(num_variables=num_variables, precision=precision, random_init=False)

                for i in range(num_variables):
                    if parent1.chromosomes[i] is not None and parent2.chromosomes[i] is not None:
                        if crossover_method == "single_point":
                            child1_chrom, child2_chrom = single_point_crossover(
                                parent1.chromosomes[i], parent2.chromosomes[i]
                            )
                        elif crossover_method == "two_point":
                            child1_chrom, child2_chrom = two_point_crossover(
                                parent1.chromosomes[i], parent2.chromosomes[i]
                            )
                        else:
                            child1_chrom, child2_chrom = uniform_crossover(
                                parent1.chromosomes[i], parent2.chromosomes[i]
                            )
                        
                        if child1_chrom is not None and child2_chrom is not None:
                            child1.chromosomes[i] = child1_chrom
                            child2.chromosomes[i] = child2_chrom
                        else:
                            child1.chromosomes[i] = Chromosome(parent1.chromosomes[i].get_chromosome_len(), False)
                            child1.chromosomes[i].set_chromosome(parent1.chromosomes[i].chromosome.copy())
                            
                            child2.chromosomes[i] = Chromosome(parent2.chromosomes[i].get_chromosome_len(), False)
                            child2.chromosomes[i].set_chromosome(parent2.chromosomes[i].chromosome.copy())

                if len(new_population) < population_size - elitism_count:
                    new_population.append(child1)
                if len(new_population) < population_size - elitism_count:
                    new_population.append(child2)
            else:
                if len(new_population) < population_size - elitism_count:
                    child1 = Individual(num_variables=num_variables, precision=precision, random_init=False)
                    for i in range(num_variables):
                        if parent1.chromosomes[i] is not None:
                            child1.chromosomes[i].set_chromosome(parent1.chromosomes[i].chromosome.copy())
                    new_population.append(child1)
                
                if len(new_population) < population_size - elitism_count:
                    child2 = Individual(num_variables=num_variables, precision=precision, random_init=False)
                    for i in range(num_variables):
                        if parent2.chromosomes[i] is not None:
                            child2.chromosomes[i].set_chromosome(parent2.chromosomes[i].chromosome.copy())
                    new_population.append(child2)

        for ind in new_population:
            ind.apply_mutation(mutation_rate, method=config.mutation_method)

        for ind in new_population:
            for i in range(ind.num_variables):
                if ind.chromosomes[i] is not None:
                    inversion(ind.chromosomes[i], inversion_rate)

        new_population.extend(elites)

        for ind in new_population:
            ind.evaluate(evaluate_fitness)

        population = new_population

        current_best = optimization_func(population, key=lambda ind: ind.fitness)
        
        avg_fitness = sum(ind.fitness for ind in population) / len(population)
        
        plotter.update_history(current_best.fitness, avg_fitness)
        
        if (config.optimization_type == "max" and current_best.fitness > best_individual.fitness) or \
           (config.optimization_type == "min" and current_best.fitness < best_individual.fitness):
            best_individual = current_best

        if generation % 10 == 0:
            print(f"Epoka {generation}, najlepsze przystosowanie: {best_individual.fitness}")

    best_individual.evaluate(evaluate_fitness)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania algorytmu: {execution_time:.2f} sekund")

    plotter.show_results_window(best_individual, execution_time)

    return best_individual, execution_time, plotter