# Networking code for the game engine
# Server to handle multiplayer connections and data exchange
# Client to connect to the server and communicate player movements and retreive other players' data
import socket
import threading
import pickle

class GameClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        threading.Thread(target=self.listen_for_server_messages).start()

    def listen_for_server_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    self.handle_server_message(pickle.loads(data))
            except Exception as e:
                print(f"Error receiving server message: {e}")
                self.running = False

    def handle_server_message(self, message):
        # Handle incoming messages from the server
        print(f"Received message from server: {message}")

    def send_player_data(self, player_data):
        try:
            self.client_socket.sendall(pickle.dumps(player_data))
        except Exception as e:
            print(f"Error sending player data: {e}")

    def disconnect(self):
        self.running = False
        self.client_socket.close()
        print("Disconnected from server")

class GameServer:
    def __init__(self, host='', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = True

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients).start()
        threading.Thread(target=self.console).start()

    def accept_clients(self):
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f"Client connected from {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(1024)
                if data:
                    player_data = pickle.loads(data)
                    self.broadcast_data(player_data)
            except Exception as e:
                print(f"Client error: {e}")
                self.handle_client_disconnect(client_socket)
                return -1

    def broadcast_data(self, player_data):
        for client in self.clients:
            try:
                client.sendall(pickle.dumps(player_data))
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def handle_client_disconnect(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()
            print("Client disconnected")

    def console(self):
        while self.running:
            command = input("Server Command> ")
            if command.lower() == "stop":
                self.broadcast_data({"type": "shutdown"})
                self.stop()
                self.running = False

    def stop(self):
        self.running = False
        self.server_socket.close()
        for client in self.clients:
            client.close()
        print("Server stopped")