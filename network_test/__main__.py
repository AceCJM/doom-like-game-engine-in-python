from engine import GameServer, GameClient

def start_server():
    server = GameServer(host='0.0.0.0', port=5555)
    server.start()
    return server
def start_client():
    client = GameClient(server_ip='10.10.21.51', server_port=5555)
    client.connect()
    return client

if __name__ == "__main__": 
    from sys import argv
    if len(argv) > 1 and argv[1] == '--server':
        server = start_server()
    else:
        client = start_client()
        # Keep the main thread alive to maintain server and client
        try:
            while True:
                message = input("Enter message to send (or 'exit' to quit): ")

                if message.lower() == 'exit':
                    client.disconnect()
                    break
                client.send_data({"type": "chat", "data": message})
        except KeyboardInterrupt:
            print("Shutting down...")
            client.disconnect()
