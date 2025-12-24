import pygame, math
from engine.map import GameMap
from engine.player import Player

mouse_sensitivity = 0.1

class GameEngine:
    def __init__(self, title="Game Engine", width=800, height=600, fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.player = None
        self.game_map = None
        
        # Grab Mouse
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def load_map(self, map_file):
        self.game_map = GameMap()
        self.game_map.load_map(map_file)
        return True

    def spawn_player(self, player_name, health=100, position=(0, 0, 0)):
        self.player = Player(name=player_name, health=health, position=position)
        return True
    
    def run(self):
        while self.running:
            print(self.player.position)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
            # Handle other events like player movement here
            keys = pygame.key.get_pressed()
            if self.player:
                if keys[pygame.K_w]:
                    # check if the player can move forward
                    if self.game_map.is_position_valid(self.player.position[0] + 0.1 * math.cos(math.radians(self.player.position[2])),
                                                       self.player.position[1] + 0.1 * math.sin(math.radians(self.player.position[2]))):
                        self.player.move(0.1 * math.cos(math.radians(self.player.position[2])),
                                     0.1 * math.sin(math.radians(self.player.position[2])))
                if keys[pygame.K_s]:
                    if self.game_map.is_position_valid(self.player.position[0] - 0.1 * math.cos(math.radians(self.player.position[2])),
                                                       self.player.position[1] - 0.1 * math.sin(math.radians(self.player.position[2]))):
                        self.player.move(-0.1 * math.cos(math.radians(self.player.position[2])),
                                         -0.1 * math.sin(math.radians(self.player.position[2])))
                if keys[pygame.K_d]:
                    if self.game_map.is_position_valid(self.player.position[0] - 0.05 * math.sin(math.radians(self.player.position[2])),
                                                       self.player.position[1] + 0.05 * math.cos(math.radians(self.player.position[2]))):
                        self.player.move(-0.05 * math.sin(math.radians(self.player.position[2])),
                                         0.05 * math.cos(math.radians(self.player.position[2])))
                if keys[pygame.K_a]:
                    if self.game_map.is_position_valid(self.player.position[0] + 0.05 * math.sin(math.radians(self.player.position[2])),
                                                       self.player.position[1] - 0.05 * math.cos(math.radians(self.player.position[2]))):
                        self.player.move(0.05 * math.sin(math.radians(self.player.position[2])),
                                         -0.05 * math.cos(math.radians(self.player.position[2])))
            # Handle mouse movement for rotation
            if self.player:
                rel_x, rel_y = pygame.mouse.get_rel()
                self.player.rotate(rel_x * mouse_sensitivity)

            self.screen.fill((0, 0, 0))  # Clear screen with black
            # draw line for wall size based on distance away from player
            map_data = self.game_map.get_map()
            if map_data and self.player:
                player_x, player_y, player_r = self.player.position
                wall_data = map_data.get("data", {}).get("walls", [])
                map_length = map_data.get("data", {}).get("map_size", {}).get("length", 0)
                map_width = map_data.get("data", {}).get("map_size", {}).get("width", 0)
                for ray in range(0, 800, 2):  # Cast rays for each vertical line
                    ray_angle = (player_r - 30) + (ray / 800) * 60  # FOV of 60 degrees
                    ray_angle_rad = ray_angle * (3.14159 / 180)
                    for depth in range(1, 800):
                        target_x = int(player_x + depth * 0.1 * math.cos(ray_angle_rad))
                        target_y = int(player_y + depth * 0.1 * math.sin(ray_angle_rad))
                        if 0 <= target_x < map_length and 0 <= target_y < map_width:
                            if wall_data[target_y][target_x] == 1:  # Wall hit
                                wall_height = max(1, int(600 / (depth * 0.1)))  # Simple perspective
                                color = (255 - min(255, depth), 0, 0)  # Darker with distance
                                pygame.draw.line(self.screen, color,
                                                 (ray, 300 - wall_height // 2),
                                                 (ray, 300 + wall_height // 2))
                                break
                
                
            pygame.display.flip()  # Update the display
            self.clock.tick(self.fps)  # Maintain specified FPS

        pygame.quit()