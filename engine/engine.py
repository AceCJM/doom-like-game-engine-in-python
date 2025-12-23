import pygame
from engine.map import GameMap
from engine.player import Player

class GameEngine:
    def __init__(self, title="Game Engine", width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Clear screen with black
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Maintain 60 FPS

        pygame.quit()