# Import external modules
import pygame
import math

# Import internal modules
from engine.map import GameMap
from engine.player import Player
from engine.network import GameServer, GameClient
from engine.pygame_widgets import Button


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
        self.look_sensitivity = 0.1
        self.game_type = ""
        
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

    def main_menu(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        menu_running = True
        font = pygame.font.SysFont(None, 75)
        title_text = font.render('Main Menu', True, (255, 255, 255))
        multiplayer_text = font.render('Multiplayer', True, (255, 255, 255))
        singleplayer_text = font.render('Single Player', True, (255, 255, 255))
        button_width = 300
        button_height = 50
        button_y = 250
        singleplayer_button = Button((255, 0, 0), 250, button_y, button_width, button_height, text='Single Player')
        multiplayer_button = Button((0, 0, 255), 250, button_y + 100, button_width, button_height, text='Multiplayer')

        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu_running = False  # Start Single Player
                        self.game_type = "sp"
                    if event.key == pygame.K_2:
                        menu_running = False  # Start Multiplayer
                        self.game_type = "mp"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if singleplayer_button.isOver(pos):
                        menu_running = False
                        self.game_type = "sp"
                    if multiplayer_button.isOver(pos):
                        menu_running = False
                        self.game_type = "mp"
            self.screen.fill((0, 0, 0))
            self.screen.blit(title_text, (300, 100))
            singleplayer_button.draw(self.screen)
            multiplayer_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(15)

    def multiplayer_menu(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        menu_running = True
        font = pygame.font.SysFont(None, 55)
        join_button = Button((0, 255, 0), 200, self.screen.get_height() - 200, 400, 50, text='Join Server')
        host_button = Button((0, 0, 255), 200, self.screen.get_height() - 100, 400, 50, text='Host Server')
        user_text = ""
        while menu_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if join_button.isOver(pos):
                        menu_running = False
                        self.multi_player_run(user_text)
                    elif host_button.isOver(pos):
                        menu_running = False
                        self.server_instance = GameServer(host='localhost', port=5555)
                        game_map = GameMap()
                        game_map.load_map("example_game/maps/default_map.json")
                        self.server_instance.start(game_map)
                        self.hosted = True
                        self.multi_player_run("localhost")
            self.screen.fill((0, 0, 0))
            ip_text = font.render('Enter Server IP: ' + user_text, True, (255, 255, 255))
            self.screen.blit(ip_text, (50, 200))
            host_button.draw(self.screen)
            join_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(15)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def pause_menu(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        paused = True
        font = pygame.font.SysFont(None, 55)
        pause_text = font.render('Game Paused. Press Esc to Resume.', True, (255, 255, 255))
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
            self.screen.fill((0, 0, 0))
            self.screen.blit(pause_text, (100, 250))
            # Draw a slider for look sensitivity adjustment
            look_sensitivity_text = font.render('Look Sensitivity:', True, (255, 255, 255))
            self.screen.blit(look_sensitivity_text, (150, 300))
            pygame.draw.rect(self.screen, (100, 100, 100), (150, 350, 500, 20))
            pygame.draw.rect(self.screen, (200, 200, 200), (150 + int(self.look_sensitivity * 500), 345, 10, 30))
            # Handle mouse input for slider
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 150 <= mouse_x <= 650 and 345 <= mouse_y <= 375:
                    self.look_sensitivity = (mouse_x - 150) / 500.0
            pygame.display.flip()
            self.clock.tick(15)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def single_player_run(self, map_name="example_game/maps/default_map.json"):
        self.game_map = GameMap()
        self.game_map.load_map(map_name)
        self.spawn_player("Player1", position=self.game_map.get_starting_position())
        while self.running:
            print(self.player.position)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()
            # Handle other events like player movement here
            keys = pygame.key.get_pressed()
            if self.player:
                # Handle WASD movement
                if keys[pygame.K_w]:
                    if self.game_map.is_position_valid(self.player.position[0] + 0.1 * math.cos(math.radians(self.player.position[2])), self.player.position[1] + 0.1 * math.sin(math.radians(self.player.position[2]))):
                        self.player.move(0.1 * math.cos(math.radians(self.player.position[2])), 0.1 * math.sin(math.radians(self.player.position[2])))
                if keys[pygame.K_s]:
                    if self.game_map.is_position_valid(self.player.position[0] - 0.1 * math.cos(math.radians(self.player.position[2])), self.player.position[1] - 0.1 * math.sin(math.radians(self.player.position[2]))):
                        self.player.move(-0.1 * math.cos(math.radians(self.player.position[2])), -0.1 * math.sin(math.radians(self.player.position[2])))
                if keys[pygame.K_d]:
                    if self.game_map.is_position_valid(self.player.position[0] - 0.05 * math.sin(math.radians(self.player.position[2])), self.player.position[1] + 0.05 * math.cos(math.radians(self.player.position[2]))):
                        self.player.move(-0.05 * math.sin(math.radians(self.player.position[2])), 0.05 * math.cos(math.radians(self.player.position[2])))
                if keys[pygame.K_a]:
                    if self.game_map.is_position_valid(self.player.position[0] + 0.05 * math.sin(math.radians(self.player.position[2])), self.player.position[1] - 0.05 * math.cos(math.radians(self.player.position[2]))):
                        self.player.move(0.05 * math.sin(math.radians(self.player.position[2])), -0.05 * math.cos(math.radians(self.player.position[2])))
                # Handle rotation with arrow keys
                if keys[pygame.K_LEFT]:
                    self.player.rotate(self.look_sensitivity * -10)
                if keys[pygame.K_RIGHT]:
                    self.player.rotate(self.look_sensitivity * 10)
                # Handle mouse movement for rotation
                rel_x, rel_y = pygame.mouse.get_rel()
                self.player.rotate(rel_x * -self.look_sensitivity)

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
                                color = (255 - min(255, depth), 255 - min(255, depth), 255 - min(255, depth))  # Darker with distance
                                pygame.draw.line(self.screen, color, (ray, 300 - wall_height // 2), (ray, 300 + wall_height // 2))
                                break
            pygame.display.flip()  # Update the display
            self.clock.tick(self.fps)  # Maintain specified FPS
        pygame.quit()

    def multi_player_run(self, ip_address, port=5555):
        
        self.client_instance = GameClient(server_ip=ip_address, server_port=port)
        self.client_instance.connect()
        try:
            self.game_map = GameMap()
            map_data = self.client_instance.get_map()
            print(f"Received map data: {map_data}")
            self.game_map.retrieve_map_data(map_data)
            self.spawn_player("Player1", position=self.game_map.get_starting_position())
            while self.running:
                print(self.player.position)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.client_instance.disconnect()
                        if self.hosted:
                            self.server_instance.running = False
                            self.server_instance.stop()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.pause_menu()
                # Handle other events like player movement here
                keys = pygame.key.get_pressed()
                if self.player:
                    # Handle WASD movement
                    if keys[pygame.K_w]:
                        if self.game_map.is_position_valid(self.player.position[0] + 0.1 * math.cos(math.radians(self.player.position[2])), self.player.position[1] + 0.1 * math.sin(math.radians(self.player.position[2]))):
                            self.player.move(0.1 * math.cos(math.radians(self.player.position[2])), 0.1 * math.sin(math.radians(self.player.position[2])))
                    if keys[pygame.K_s]:
                        if self.game_map.is_position_valid(self.player.position[0] - 0.1 * math.cos(math.radians(self.player.position[2])), self.player.position[1] - 0.1 * math.sin(math.radians(self.player.position[2]))):
                            self.player.move(-0.1 * math.cos(math.radians(self.player.position[2])), -0.1 * math.sin(math.radians(self.player.position[2])))
                    if keys[pygame.K_d]:
                        if self.game_map.is_position_valid(self.player.position[0] - 0.05 * math.sin(math.radians(self.player.position[2])), self.player.position[1] + 0.05 * math.cos(math.radians(self.player.position[2]))):
                            self.player.move(-0.05 * math.sin(math.radians(self.player.position[2])), 0.05 * math.cos(math.radians(self.player.position[2])))
                    if keys[pygame.K_a]:
                        if self.game_map.is_position_valid(self.player.position[0] + 0.05 * math.sin(math.radians(self.player.position[2])), self.player.position[1] - 0.05 * math.cos(math.radians(self.player.position[2]))):
                            self.player.move(0.05 * math.sin(math.radians(self.player.position[2])), -0.05 * math.cos(math.radians(self.player.position[2])))
                    # Handle rotation with arrow keys
                    if keys[pygame.K_LEFT]:
                        self.player.rotate(self.look_sensitivity * -10)
                    if keys[pygame.K_RIGHT]:
                        self.player.rotate(self.look_sensitivity * 10)
                    # Handle mouse movement for rotation
                    rel_x, rel_y = pygame.mouse.get_rel()
                    self.player.rotate(rel_x * -self.look_sensitivity)

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
                                    color = (255 - min(255, depth), 255 - min(255, depth), 255 - min(255, depth))  # Darker with distance
                                    pygame.draw.line(self.screen, color, (ray, 300 - wall_height // 2), (ray, 300 + wall_height // 2))
                                    break
                # Send player position to server
                self.client_instance.send_data({"type": "player_update", "data": {"player_id": self.client_instance.player_id, "position": self.player.position}})
                # Render other players based on data given to the client instance
                for other_player in self.client_instance.otherplayers.values():
                    # Simple representation: draw a rectangle at other player's position
                    other_x, other_y, _ = other_player['position']
                    screen_x = int((other_x - self.player.position[0]) * 50 + 400)  # Scale and center
                    screen_y = int((other_y - self.player.position[1]) * 50 + 300)
                    pygame.draw.rect(self.screen, (0, 255, 0), (screen_x - 5, screen_y - 5, 10, 10))
                pygame.display.flip()  # Update the display
                self.clock.tick(self.fps)  # Maintain specified FPS
        except Exception as e:
            print(f"Error in multiplayer run: {e}")
            self.client_instance.disconnect()
            if self.hosted:
                self.server_instance.running = False
                self.server_instance.stop()
    
    def run(self):
        self.main_menu()
        if self.game_type == "mp":
            self.multiplayer_menu()
            # For simplicity, directly start multiplayer with localhost
            # self.multi_player_run("localhost", 5555)
        elif self.game_type == "sp":
            self.single_player_run()
        pygame.quit()