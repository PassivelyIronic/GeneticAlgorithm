import random
import numpy as np
from algorithms.chromosome import Chromosome

def single_point_crossover(parent1: Chromosome, parent2: Chromosome):

    if parent1 is None or parent2 is None:
        print("Ostrzeżenie: Jeden z rodziców jest None")
        return None, None
    
    if not isinstance(parent1, Chromosome) or not isinstance(parent2, Chromosome):
        print("Ostrzeżenie: Rodzice muszą być obiektami klasy Chromosome")
        return None, None
        
    if parent1.get_chromosome_len() != parent2.get_chromosome_len():
        print("Ostrzeżenie: Chromosomy rodziców mają różne długości")
        return None, None
    
    point = random.randint(1, parent1.get_chromosome_len() - 1)
    
    child1 = Chromosome(parent1.get_chromosome_len(), random_init=False)
    child2 = Chromosome(parent2.get_chromosome_len(), random_init=False)
    
    child1_chromosome = parent1.chromosome[:point] + parent2.chromosome[point:]
    child2_chromosome = parent2.chromosome[:point] + parent1.chromosome[point:]
    
    child1.set_chromosome(child1_chromosome)
    child2.set_chromosome(child2_chromosome)
    
    return child1, child2

def two_point_crossover(parent1: Chromosome, parent2: Chromosome):

    if parent1 is None or parent2 is None:
        print("Ostrzeżenie: Jeden z rodziców jest None")
        return None, None
    
    if not isinstance(parent1, Chromosome) or not isinstance(parent2, Chromosome):
        print("Ostrzeżenie: Rodzice muszą być obiektami klasy Chromosome")
        return None, None
        
    if parent1.get_chromosome_len() != parent2.get_chromosome_len():
        print("Ostrzeżenie: Chromosomy rodziców mają różne długości")
        return None, None
    
    length = parent1.get_chromosome_len()
    
    if length < 3:
        print("Ostrzeżenie: Chromosomy są zbyt krótkie dla krzyżowania dwupunktowego")
        return None, None
    
    point1 = random.randint(1, length - 2)
    point2 = random.randint(point1 + 1, length - 1)

    child1 = Chromosome(length, random_init=False)
    child2 = Chromosome(length, random_init=False)
    
    child1.set_chromosome(parent1.chromosome[:point1] + parent2.chromosome[point1:point2] + parent1.chromosome[point2:])
    child2.set_chromosome(parent2.chromosome[:point1] + parent1.chromosome[point1:point2] + parent2.chromosome[point2:])
    
    return child1, child2

def uniform_crossover(parent1: Chromosome, parent2: Chromosome):
    if parent1 is None or parent2 is None:
        print("Ostrzeżenie: Jeden z rodziców jest None")
        return None, None
    
    if not isinstance(parent1, Chromosome) or not isinstance(parent2, Chromosome):
        print("Ostrzeżenie: Rodzice muszą być obiektami klasy Chromosome")
        return None, None
        
    if parent1.get_chromosome_len() != parent2.get_chromosome_len():
        print("Ostrzeżenie: Chromosomy rodziców mają różne długości")
        return None, None
    
    child1 = Chromosome(parent1.get_chromosome_len(), random_init=False)
    child2 = Chromosome(parent2.get_chromosome_len(), random_init=False)
    
    new_chromosome1 = []
    new_chromosome2 = []
    
    for i in range(parent1.get_chromosome_len()):
        if random.random() < 0.5:
            new_chromosome1.append(parent1.chromosome[i])
            new_chromosome2.append(parent2.chromosome[i])
        else:
            new_chromosome1.append(parent2.chromosome[i])
            new_chromosome2.append(parent1.chromosome[i])
    
    child1.set_chromosome(new_chromosome1)
    child2.set_chromosome(new_chromosome2)
    
    return child1, child2