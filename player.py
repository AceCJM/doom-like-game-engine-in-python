"""
Player class for handling position, rotation, and movement
"""
import pygame
import math
from settings import PLAYER_SPEED, PLAYER_ROT_SPEED


class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle  # Player's viewing angle in radians

    def move(self, game_map, keys):
        """Handle player movement based on keyboard input"""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        
        dx, dy = 0, 0
        speed = PLAYER_SPEED
        
        # Forward/backward movement (W/S keys)
        if keys[pygame.K_w]:
            dx += cos_a * speed
            dy += sin_a * speed
        if keys[pygame.K_s]:
            dx -= cos_a * speed
            dy -= sin_a * speed
        
        # Strafe left/right (A/D keys)
        if keys[pygame.K_a]:
            dx += sin_a * speed
            dy -= cos_a * speed
        if keys[pygame.K_d]:
            dx -= sin_a * speed
            dy += cos_a * speed
        
        # Check collision before moving
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Only move if not colliding with walls
        if not game_map.is_wall(new_x, self.y):
            self.x = new_x
        if not game_map.is_wall(self.x, new_y):
            self.y = new_y
        
        # Rotation (Arrow keys)
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED
        
        # Keep angle in range [0, 2*PI]
        self.angle = self.angle % (2 * math.pi)
