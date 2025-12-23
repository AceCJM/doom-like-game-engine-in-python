"""
Renderer for drawing the 3D view
"""
import pygame
from settings import (
    WIDTH, HEIGHT, WALL_COLORS, FLOOR_COLOR, CEILING_COLOR, NUM_RAYS
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = WIDTH
        self.screen_height = HEIGHT

    def draw_background(self):
        """Draw floor and ceiling"""
        # Draw ceiling
        pygame.draw.rect(
            self.screen, CEILING_COLOR, 
            (0, 0, self.screen_width, self.screen_height // 2)
        )
        # Draw floor
        pygame.draw.rect(
            self.screen, FLOOR_COLOR, 
            (0, self.screen_height // 2, self.screen_width, self.screen_height // 2)
        )

    def draw_walls(self, rays):
        """Draw walls based on raycasting results"""
        wall_width = self.screen_width / NUM_RAYS
        
        for i, (depth, wall_type) in enumerate(rays):
            # Calculate wall height based on distance
            # Prevent division by zero
            if depth < 0.01:
                depth = 0.01
            
            wall_height = min(int(self.screen_height / depth), self.screen_height * 2)
            
            # Get wall color
            color = WALL_COLORS.get(wall_type, (128, 128, 128))
            
            # Apply distance-based shading (darker when farther)
            shade_factor = max(0.2, 1 - (depth / 15))
            shaded_color = tuple(int(c * shade_factor) for c in color)
            
            # Draw the wall strip
            wall_x = i * wall_width
            wall_y = (self.screen_height - wall_height) // 2
            
            pygame.draw.rect(
                self.screen, shaded_color,
                (wall_x, wall_y, wall_width + 1, wall_height)
            )

    def draw_minimap(self, game_map, player):
        """Draw a 2D minimap in the corner"""
        minimap_scale = 8
        minimap_offset_x = 10
        minimap_offset_y = 10
        
        # Draw map tiles
        for y, row in enumerate(game_map.world_map):
            for x, tile in enumerate(row):
                if tile != 0:
                    color = WALL_COLORS.get(tile, (128, 128, 128))
                    pygame.draw.rect(
                        self.screen, color,
                        (
                            minimap_offset_x + x * minimap_scale,
                            minimap_offset_y + y * minimap_scale,
                            minimap_scale,
                            minimap_scale
                        )
                    )
        
        # Draw player position
        player_minimap_x = minimap_offset_x + int(player.x * minimap_scale)
        player_minimap_y = minimap_offset_y + int(player.y * minimap_scale)
        pygame.draw.circle(
            self.screen, (255, 255, 0),
            (player_minimap_x, player_minimap_y),
            3
        )

    def render(self, rays, game_map, player, show_minimap=True):
        """Main rendering function"""
        self.draw_background()
        self.draw_walls(rays)
        if show_minimap:
            self.draw_minimap(game_map, player)
