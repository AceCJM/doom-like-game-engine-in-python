"""
Raycasting engine for 3D rendering
"""
import math
from settings import (
    FOV, HALF_FOV, NUM_RAYS, MAX_DEPTH, DELTA_ANGLE, TILE_SIZE
)


class Raycaster:
    def __init__(self, game_map):
        self.game_map = game_map

    def cast_rays(self, player):
        """Cast rays from the player's position and return wall distances"""
        rays = []
        
        # Start from the leftmost ray
        ray_angle = player.angle - HALF_FOV
        
        for ray in range(NUM_RAYS):
            # Calculate ray direction
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            
            # Cast the ray
            depth = 0
            wall_type = 0
            
            # Step along the ray until we hit a wall or reach max depth
            for depth in range(1, int(MAX_DEPTH * 100)):
                depth_f = depth / 100.0
                
                # Calculate target position
                target_x = player.x + cos_a * depth_f
                target_y = player.y + sin_a * depth_f
                
                # Check if we hit a wall
                tile = self.game_map.get_tile(target_x, target_y)
                if tile != 0:
                    wall_type = tile
                    depth = depth_f
                    break
            else:
                depth = MAX_DEPTH
            
            # Fix fish-eye effect by using perpendicular distance
            depth *= math.cos(player.angle - ray_angle)
            
            rays.append((depth, wall_type))
            ray_angle += DELTA_ANGLE
        
        return rays
