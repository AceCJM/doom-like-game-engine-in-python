import engine
from sys import argv

if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == '--server':
        server = engine.GameServer(host='0.0.0.0', port=5555)
        game_map = engine.GameMap()
        game_map.load_map("example_game/maps/default_map.json")
        server.start(game_map)
    else:
        game = engine.GameEngine(width=800, height=600, title="Example Game")
        game.run()