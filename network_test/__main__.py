from engine import Server, Client
import threading

# Start the server in a separate thread
def start_server():
    server = Server(host='127.0.0.1', port=5555)
    server.accept_clients()

server_thread = threading.Thread(target=start_server)
server_thread.start()

# Create a client and connect to the server
client = Client(server_ip='127.0.0.1', server_port=5555)
client.send("Hello, Server!")
