import pygame
from simulation.simulation import Simulation

def main():
    session = Simulation(population_size = 10)
    while session.running:
        session.keep_fps(60.0)
        session.handle_events()
        session.render()
    session.cleanup()


if __name__ == '__main__':
    main()