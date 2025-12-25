from engine import GameServer, GameClient

def start_server():
    server = GameServer(host='localhost', port=5555)
    server.start()
    return server
def start_client():
    client = GameClient(server_ip='localhost', server_port=5555)
    client.connect()
    return client

if __name__ == "__main__":
    server = start_server()
    client = start_client()
    # Keep the main thread alive to maintain server and client
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
        client.disconnect()
        server.stop()
