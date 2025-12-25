from engine import GameServer, GameClient

def start_server():
    server = GameServer(host='0.0.0.0', port=5555)
    server.start()
    return server
def start_client():
    client = GameClient(server_ip='localhost', server_port=5555)
    client.connect()
    return client

if __name__ == "__main__":
    server = start_server()
