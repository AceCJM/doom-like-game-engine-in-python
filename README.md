# Doom-like Game Engine in Python

A simple 3D raycasting game engine built with Python and Pygame, inspired by classic games like Doom. This engine provides basic functionality for creating first-person perspective games with map loading, player movement, and wall rendering.

## Features

- **Raycasting Rendering**: Implements basic raycasting for 3D-like wall rendering
- **Player Movement**: WASD movement with collision detection
- **Mouse Look**: Mouse-based camera rotation with adjustable sensitivity
- **Map Loading**: Load game maps from JSON files
- **Pause Menu**: In-game pause functionality with sensitivity adjustment
- **Modular Design**: Clean separation of engine components (map, player, engine)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AceCJM/doom-like-game-engine-in-python.git
   cd doom-like-game-engine-in-python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Example Game

To run the included example game:

```bash
python -m example_game
```

This will start a simple game with a basic map.

### Using the Engine in Your Project

```python
import engine

# Create a game instance
game = engine.GameEngine(width=800, height=600, title="My Game")

# Load a map
game.load_map("path/to/your/map.json")

# Spawn a player
game.spawn_player("Player", health=100, position=(x, y, rotation))

# Run the game loop
game.run()
```

### Map Format

Maps are stored in JSON format. See `example_game/maps/example_map.json` for an example structure:

```json
{
  "data": {
    "map_size": {
      "length": 10,
      "width": 10,
      "starting_position": [1.5, 1.5, 0]
    },
    "walls": [
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      ...
    ]
  }
}
```

- `map_size`: Dimensions of the map (length x width)
- `walls`: 2D array where 1 represents a wall and 0 represents empty space
- `starting_position`: [x, y, rotation] for player spawn

## Controls

- **WASD**: Move forward/backward and strafe left/right
- **Arrow Keys**: Rotate left/right
- **Mouse**: Look around (rotation)
- **ESC**: Pause/unpause the game
- In pause menu, click and drag the slider to adjust mouse sensitivity

## Project Structure

```
doom-like-game-engine-in-python/
├── engine/
│   ├── __init__.py
│   ├── engine.py       # Main game engine
│   ├── map.py          # Map loading and collision detection
│   └── player.py       # Player class with movement
├── example_game/
│   ├── __init__.py
│   ├── __main__.py     # Example game implementation
│   └── maps/
│       └── example_map.json
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

## Requirements

- Python 3.6+
- Pygame 2.6.1

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.