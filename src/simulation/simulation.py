from game.FlappyBird import FlappyBird
import pygame


class Simulation:
    SCREEN_SIZE = (1280, 720)
    BACKGROUND_COL = (37, 37, 48)

    def __init__(self, population_size=10):
        pygame.init()
        self.population_size = population_size
        self.screen = pygame.display.set_mode(Simulation.SCREEN_SIZE)
        self.flappy_bird = FlappyBird(*Simulation.SCREEN_SIZE, population_size)
        self.clock = pygame.time.Clock()
        self.running = True


    def render(self):
        self.flappy_bird.update()
        self.screen.fill(Simulation.BACKGROUND_COL)
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
        self.flappy_bird.render(self.screen)
        pygame.display.flip()


    def keep_fps(self, fps=60.0):
        self.clock.tick(fps)
    

    def handle_events(self, navigation=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if navigation and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.flappy_bird.jump(0)
                if event.key == pygame.K_UP:
                    self.flappy_bird.jump(1)
                if event.key == pygame.K_m:
                    self.flappy_bird.reset(10)


    def cleanup(self):
        pygame.quit()