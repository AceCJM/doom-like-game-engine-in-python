class GameMap:
    def __init__(self):
        self.map_data = []
    
    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            self.map_data = [line.strip() for line in f.readlines()]
    
    def get_map(self):
        return self.map_data