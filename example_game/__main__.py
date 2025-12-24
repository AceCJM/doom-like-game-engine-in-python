import engine

if __name__ == "__main__":
    game = engine.GameEngine(width=800, height=600, title="Example Game")
    if game.load_map("example_game/maps/example_map.json"):
        game.spawn_player("Hero", health=100, position=game.game_map.get_starting_position())
        game.run()