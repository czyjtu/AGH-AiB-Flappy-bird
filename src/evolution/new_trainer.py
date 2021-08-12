from simulation.simulation import Simulation
from evolution.utils import roulette_wheel_selection

class GeneticTrainer(Simulation):
    def __init__(
        self, population_size=50, max_generation=100, 
        scale_start=0.9, scale_end=0.01, 
        crossover_method='one_point', selection_method='roulette'
        ):

        super().__init__(population_size)
        self.scale_start = scale_start
        self.scale_end = scale_end
        self.max_generation = max_generation

        self.crossover_method = crossover_method
        self.selection_method = selection_method


    def train(self):
        self.population = self.get_initial_population()
        self.epoch = 0
        while self.is_termination_criteria_satisfied():
            self.game.reset(self.population_size)
            self.epoch += 1
            self.birds = self.game.get_birds()
            while self.running:
                self.keep_fps(float('inf'))
                self.handle_events()
                self.render()

                self._make_moves()
                self.calculate_fitness()
                self.running = self.is_termination_criteria_satisfied()
                parents = self.selection()
                childs = self.crossover(parents)
                self.population = self.mutation(childs)
        self.cleanup()


    def get_initial_population(self):
        return {(self.new_network(), i) for i in range(self.population_size)}

    
    def calculate_fitness(self):
        pass

    
    def selection(self):
        if self.selection_method == 'roulette':
            parents = [
                [roulette_wheel_selection(self.population, lambda n: n.score) for _ in range(2)] for _ in range(self.population_size // 2)
                ]
        return parents


    # TODO: functions to cross individuals instead of 
    def crossover(self, parents):
        if self.crossover_method == 'one_point':
            pass
        


    def mutation(self):
        pass


     def new_network(self):
        # x rury, y1 rury, y2 rury, y ptaka, y vel ptaka
        model = NeuralNetwork([
            Dense(size=(5, 5), activation='elu'),
            Dense((5, 1), activation='sigmoid')
        ])
        return model


    def _make_moves(self):
        closest_pipe = self.game.get_obstacle()
        horizontal_dist = closest_pipe[0] - self.birds[0].X_POSITION # every bird has the same x coordinate so pick the first one
        y1, y2 = closest_pipe[0][1], closest_pipe[1][1]

        for network, bird_idx in self.population:
            self.jump_or_not_to_jump(horizontal_dist, y1, y2, network, bird_idx)
        


    def jump_or_not_to_jump(self, horizontal_dist, y1, y2, network, bird_idx):
        input = np.array([[
            horizontal_dist / 700,
            self.birds[bird_idx].y_position / 720,
            y1 / 720,
            y2 / 720,
            bird.y_velocity * 5 / max_vel
        ]])
        if network.predict(input) > 0.5 and not self.birds[i].lost:
            self.game.jump(bird_idx)
            

    def _update_scale(self):
        self.scale = self.scale - (self.scale_start - self.scale_end) / self.max_gen


    def _setup_playground(self):
        self.best_score = 0
        self.best_network = self.networks[0]

        self.scale_decay = (self.scale_end - self.scale_start) / max_generation
        self.scale = self.scale_start
