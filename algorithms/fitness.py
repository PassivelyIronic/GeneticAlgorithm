import numpy as np
from algorithms.config import config
from algorithms.individual import Individual

def hypersphere(individual: Individual) -> float:

    if individual.chromosome_values is None or len(individual.chromosome_values) == 0:
        print("Ostrzeżenie: chromosome_values jest None lub puste")
        return float('inf')
        
    return sum(xi ** 2 for xi in individual.chromosome_values)

def martin_and_gaddy(individual: Individual):
    
    if individual.chromosome_values is None:
        print("Ostrzeżenie: chromosome_values jest None")
        return float('inf') 
    
    if len(individual.chromosome_values) < 2:
        print("Ostrzeżenie: chromosome_values ma mniej niż 2 elementy")
        return float('inf')
        
    x1, x2 = individual.chromosome_values[:2]
    return (x1 - x2) ** 2 + ((x1 + x2 - 10) / 3) ** 2


def evaluate_fitness(individual: Individual):
    
    if config.function == "Martin and Gaddy":
        return martin_and_gaddy(individual)
    elif config.function == "hypersphere":
        return hypersphere(individual)
    else:
        print(f"Ostrzeżenie: Nieznana funkcja fitness: {config.function}")
        return float('inf')