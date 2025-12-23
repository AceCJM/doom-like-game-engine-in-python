"""
Game settings and configuration constants
"""
import math

# Window settings
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Raycasting settings
FOV = math.pi / 3  # 60 degrees field of view
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # Number of rays to cast
MAX_DEPTH = 20  # Maximum ray distance
DELTA_ANGLE = FOV / NUM_RAYS

# Player settings
PLAYER_SPEED = 0.05
PLAYER_ROT_SPEED = 0.03

# Map settings
TILE_SIZE = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Wall colors
WALL_COLORS = {
    1: GRAY,
    2: RED,
    3: GREEN,
    4: BLUE,
}

# Floor and ceiling colors
FLOOR_COLOR = DARK_GRAY
CEILING_COLOR = (50, 50, 100)
