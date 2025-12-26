from engine import GameServer, GameClient
from engine import GameMap

def start_server():
    server = GameServer(host='0.0.0.0', port=5555)
    game_map = GameMap()
    game_map.load_map("network_test/maps/default_map.json")
    server.start(game_map)
    return server
def start_client():
    client = GameClient(server_ip='10.10.21.51', server_port=5555)
    client.connect()
    return client

if __name__ == "__main__": 
    from sys import argv
    if len(argv) > 1 and argv[1] == '--server':
        server = start_server()
        # Keep the main thread alive
        try:
            while server.running:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down server...")
            server.stop()
    else:
        client = start_client()
        # Keep the main thread alive to maintain server and client
        try:
            while True:
                message = input("Enter message to send (or 'exit' to quit): ")

                if message.lower() == 'exit':
                    client.disconnect()
                    exit()
                client.send_data({"type": "chat", "data": message})
        except KeyboardInterrupt:
            print("Shutting down...")
            client.disconnect()
