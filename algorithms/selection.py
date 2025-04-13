import random

def best_selection(individuals, num_selected):
    sorted_individuals = sorted(individuals, key=lambda ind: ind.fitness)
    return [ind for ind in sorted_individuals[:num_selected] if ind is not None]

def roulette_selection(individuals, num_selected):
    total_fitness = sum(1/ind.fitness for ind in individuals if ind is not None)
    selection_probs = [(1/ind.fitness)/total_fitness for ind in individuals if ind is not None]

    selected = []
    for _ in range(num_selected):
        r = random.random()
        cumulative_prob = 0
        for i, ind in enumerate(individuals):
            if ind is not None:
                cumulative_prob += selection_probs[i]
                if r <= cumulative_prob:
                    selected.append(ind)
                    break
    return selected

def tournament_selection(individuals, tournament_size=3):
    selected = []
    for _ in range(len(individuals)):
        tournament = random.sample(individuals, tournament_size)
        winner = min(tournament, key=lambda ind: ind.fitness)
        selected.append(winner)
    return selected