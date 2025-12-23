# Doom-Like Game Engine in Python

A simple raycasting game engine inspired by Wolfenstein 3D and Doom, built with Python and Pygame.

## Features

- **Raycasting 3D rendering** - Creates a pseudo-3D environment from a 2D map
- **First-person movement** - WASD controls for movement, arrow keys for rotation
- **Textured walls** - Different colored walls for visual variety
- **Collision detection** - Prevents walking through walls
- **Minimap** - Shows player position and map layout in real-time
- **FPS counter** - Displays current frames per second

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **W** - Move forward
- **S** - Move backward
- **A** - Strafe left
- **D** - Strafe right
- **Left Arrow** - Rotate left
- **Right Arrow** - Rotate right
- **ESC** - Exit game

## How It Works

This engine uses raycasting to create a 3D effect:

1. **Map System** - A 2D grid represents the game world (1 = wall, 0 = empty)
2. **Raycasting** - Rays are cast from the player's position to detect walls
3. **Rendering** - Wall heights are calculated based on distance (closer = taller)
4. **Movement** - Player position and angle are updated based on input
5. **Collision** - Checks prevent moving into walls

## Project Structure

- `main.py` - Game loop and initialization
- `settings.py` - Configuration constants
- `map.py` - Map representation and collision detection
- `player.py` - Player position, rotation, and movement
- `raycaster.py` - Raycasting algorithm for 3D rendering
- `renderer.py` - Drawing walls, floor, ceiling, and minimap

## License

See LICENSE file for details.