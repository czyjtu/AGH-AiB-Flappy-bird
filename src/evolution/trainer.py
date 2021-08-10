import random
import pygame
from network.nn import NeuralNetwork
from network.dense import Dense
from game.FlappyBird import FlappyBird
from game import SCREEN_SIZE
import numpy as np
from copy import deepcopy



"""


"""

class Trainer:
    def __init__(self, population_size=50, max_generation=100, scale_start=0.9, scale_end=0.01, crossover_method='one_point', selection_method='roulette'):
        self.population_size = population_size
        self.max_gen = max_generation
        self.current_gen = 0
        self.game = FlappyBird(*SCREEN_SIZE, self.population_size)
        self.networks = [self.new_network() for _ in range(population_size)]
        self.scale_start = scale_start
        self.scale_end = scale_end


    def _setup_playground(self):
        pygame.init()
        self.screen = pygame.display.set_mode(*SCREEN_SIZE)
        self.clock = pygame.time.Clock() 
        self.running = True

        self.best_score = 0
        self.best_network = self.networks[0]

        self.scale_decay = (self.scale_end - self.scale_start) / max_generation
        self.scale = self.scale_start


    def _render(self):
        screen.fill((37, 37, 48))
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
        self.game.render(screen)
        pygame.display.flip()


    def update_scale(self):
        self.scale = self.scale - (self.scale_start - self.scale_end) / self.max_gen


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.game.reset(10)


    def start(self):
        self._setup_playground()
        for i in range(self.max_gen):
            while self.running:
                # delta_time = clock.tick(500.0)/10
                self._handle_events()
                if self.decide(): # game over
                    break
                self.game.update()
                self._render()

            current_best_id, current_best_score = self.selection()
            self.crossover()
            self.mutation()
            print(f"generation {i}:    best score now: {current_best_score}   best score overall {self.best_score}")

            if not running:
                break

            self.game.reset(self.population_size)
        pygame.quit()


    def decide(self):
        birds = self.game.get_birds()
        pipe = self.game.get_obstacle()

        max_vel = self.game.v_max()

        x_dist = pipe[0][0] - birds[0].X_POSITION
        y1, y2 = pipe[0][1], pipe[1][1]

        all_lost = True
        for i, bird in enumerate(birds):
            if bird.lost:
                continue
            all_lost = False
            y = bird.y_position
            input = np.array([[
                x_dist / 700,
                y / 720,
                y1 / 720,
                y2 / 720,
                bird.y_velocity * 5 / max_vel
            ]])
            output = self.networks[i].predict(input)
            if output > self.tap_levels[i]:
                self.game.jump(i)
        
        return all_lost

    def selection(self):
        birds = self.game.get_birds()
        best_id =  max(range(self.population_size), key=lambda x: birds[x].score)
        best_score = birds[best_id].score
        if best_score > self.best_score:
            self.best_score = best_score
            self.best_network = self.networks[best_id]
            self.best_tap_level = self.tap_levels[best_id]
        return best_id, best_score

    def crossover(self):
        self.networks = [deepcopy(self.best_network) for _ in range(self.population_size)]
        self.tap_levels = [self.best_tap_level for _ in range(self.population_size)]

    def mutation(self):
        self.update_scale()
        for i in range(self.population_size):
            self.networks[i].mutate(amount=0.1, scale=self.scale)
            self.tap_levels[i] = self.tap_levels[i] ** (1 + self.scale * min(max(random.gauss(0, 0.1), -1), 1))


    def new_network(self):
        # x rury, y1 rury, y2 rury, y ptaka, y vel ptaka
        model = NeuralNetwork([
            Dense(size=(5, 5), activation='elu'),
            Dense((5, 1), activation='sigmoid')
        ])

        return model
