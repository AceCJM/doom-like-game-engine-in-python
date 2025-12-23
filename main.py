"""
Main game engine - Doom-like raycasting game
"""
import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, WHITE
from map import Map
from player import Player
from raycaster import Raycaster
from renderer import Renderer


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doom-like Game Engine")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.game_map = Map()
        self.player = Player(x=8.5, y=8.5, angle=0)  # Start in the middle of the map
        self.raycaster = Raycaster(self.game_map)
        self.renderer = Renderer(self.screen)
        
        # Font for FPS display
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game state"""
        keys = pygame.key.get_pressed()
        self.player.move(self.game_map, keys)

    def render(self):
        """Render the game"""
        # Cast rays
        rays = self.raycaster.cast_rays(self.player)
        
        # Render the scene
        self.renderer.render(rays, self.game_map, self.player)
        
        # Display FPS
        fps = int(self.clock.get_fps())
        fps_text = self.font.render(f'FPS: {fps}', True, WHITE)
        self.screen.blit(fps_text, (WIDTH - 120, 10))
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()
