class GameMap:
    def __init__(self):
        self.map_data = []
    
    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            from json import load
            self.map_data = load(f)
        return True
    
    def is_position_valid(self, x, y):
        map_width = self.map_data['data']['map_size']['width']
        map_length = self.map_data['data']['map_size']['length']
        grid_x = int(x)
        grid_y = int(y)
        if 0 <= grid_x < map_length and 0 <= grid_y < map_width:
            return self.map_data['data']['walls'][grid_y][grid_x] == 0  # Assuming 0 is walkable
        return False

    def get_starting_position(self):
        return self.map_data.get("details", {}).get("starting_position", (0, 0))

    def get_map(self):
        return self.map_data