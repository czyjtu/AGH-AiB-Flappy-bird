import numpy as np


def roulette_wheel_selection(population, fitness_fun):
    population_fitness = sum([fitness_fun(chromosome) for chromosome in population])
    chromosome_probabilities = [chromosome.fitness/population_fitness for chromosome in population]
    return np.random.choice(population, p=chromosome_probabilities)


