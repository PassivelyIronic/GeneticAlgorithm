class Config:
    def __init__(self):
        self.function = "Martin and Gaddy"
        self.range_start = -20
        self.range_end = 20
        self.population_size = 100
        self.precision = 5
        self.num_variables = 2
        self.epochs = 100
        self.elite_size = 2
        self.selection_method = "tournament"
        self.best_selection_amount = 5
        self.tournament_size = 3
        self.crossover_method = "single_point" 
        self.crossover_probability = 0.8
        self.mutation_method = "edge" 
        self.mutation_probability = 0.05
        self.inversion_probability = 0.1
        self.optimization_type = "min"

config = Config()
