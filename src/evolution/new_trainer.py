from simulation.simulation import Simulation

class GeneticTrainer(Simulation):
    def __init__(
        self, population_size=50, max_generation=100, 
        scale_start=0.9, scale_end=0.01, 
        crossover_method='one_point', selection_method='roulette'
        ):

        super().__init__()
        self.scale_start = scale_start
        self.scale_end = scale_end


    def train(self):
        pass


    def get_initial_population(self):
        pass

    
    def calculate_fitness(self):
        pass

    
    def selection(self):
        pass


    def crossover(self):
        pass


    def mutation(self):
        pass


    def _update_scale(self):
        self.scale = self.scale - (self.scale_start - self.scale_end) / self.max_gen


    def _setup_playground(self):
        self.best_score = 0
        self.best_network = self.networks[0]

        self.scale_decay = (self.scale_end - self.scale_start) / max_generation
        self.scale = self.scale_start
