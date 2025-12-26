# Networking code for the game engine
# Server to handle multiplayer connections and data exchange
# Client to connect to the server and communicate player movements and retreive other players' data
import socket
import threading
import json
import struct

class GameClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.otherplayers = {}  # Store other players' data
        self.running = True
        self.map_response = None

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        self.player_id = self.client_socket.getsockname()
        threading.Thread(target=self.listen_for_server_messages).start()

    def listen_for_server_messages(self):
        while self.running:
            try:
                length_data = self.client_socket.recv(4)
                if not length_data:
                    break
                length = struct.unpack('<I', length_data)[0]
                data = b''
                while len(data) < length:
                    chunk = self.client_socket.recv(min(1024, length - len(data)))
                    if not chunk:
                        break
                    data += chunk
                if len(data) == length:
                    message = json.loads(data.decode('utf-8'))
                    self.handle_server_message(message)
            except Exception as e:
                print(f"Error receiving server message: {e}")
                self.running = False

    def handle_server_message(self, data):
        print(f"Handling server message: {data}")
        if data['type'] == "shutdown":
            print("Server is shutting down.")
            self.running = False
            self.disconnect()
        elif data['type'] == "player_update":
            print(f"Player update received: {data['data']}")
            player_id = data['data']['player_id']
            self.otherplayers[player_id] = data['data']
        elif data['type'] == "map_data":
            self.map_response = data['data']
        elif data['type'] == "chat":
            print(f"Chat message received: {data['data']}")
        print(f"Received message from server: {data}")

    def send_data(self, data: dict):
        json_data = json.dumps(data).encode('utf-8')
        length = struct.pack('<I', len(json_data))
        try:
            self.client_socket.sendall(length + json_data)
        except Exception as e:
            print(f"Error sending data: {e}")

    def get_map(self):
        try:
            self.send_data({"type": "get_map"})
            import time
            start = time.time()
            while self.map_response is None and time.time() - start < 5:
                time.sleep(0.01)
            if self.map_response is None:
                print("Timeout waiting for map response")
                return None
            return self.map_response
        except Exception as e:
            print(f"Error getting map data: {e}")
            return None

    def disconnect(self):
        self.running = False
        self.send_data({"type": "socket", "data": "close"})
        self.client_socket.close()
        print("Disconnected from server")
        self.client_socket = None
class GameServer:
    def __init__(self, host='', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(1.0)
        self.clients = []
        self.running = True
        self.map = None  # Placeholder for GameMap instance

    def start(self, map_data):
        self.map = map_data
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients).start()
        threading.Thread(target=self.console).start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Client connected from {addr}")
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def handle_client(self, client_socket):
        while self.running:
            try:
                length_data = client_socket.recv(4)
                if not length_data:
                    break
                length = struct.unpack('<I', length_data)[0]
                data = b''
                while len(data) < length:
                    chunk = client_socket.recv(min(1024, length - len(data)))
                    if not chunk:
                        break
                    data += chunk
                if len(data) == length:
                    message = json.loads(data.decode('utf-8'))
                    print(f"Received data from client: {message}")
                    if message['type'] == "socket" and message['data'] == "close":
                        self.handle_client_disconnect(client_socket)
                        return -1
                    elif message['type'] == "get_map":
                        self.get_map(client_socket)
                    else:
                        self.broadcast_data(message, client_socket)
            except Exception as e:
                print(f"Client error: {e}")
                self.handle_client_disconnect(client_socket)
                return -1

    def get_map(self, client_socket):
        if self.map:
            try:
                self.send_data(client_socket, {"type": "map_data", "data": self.map.get_map()})
            except Exception as e:
                print(f"Error sending map data: {e}")

    def broadcast_data(self, data, exclude=None):
        json_data = json.dumps(data).encode('utf-8')
        length = struct.pack('<I', len(json_data))
        message = length + json_data
        clients_to_send = [c for c in self.clients if c != exclude]
        print(f"Broadcasting {data} to {len(clients_to_send)} clients")
        for client in clients_to_send:
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def send_data(self, client_socket, data):
        json_data = json.dumps(data).encode('utf-8')
        length = struct.pack('<I', len(json_data))
        message = length + json_data
        try:
            client_socket.sendall(message)
        except Exception as e:
            print(f"Error sending data to client: {e}")

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
        self.server_socket.close()
        print("Server stopped")
        exit(0)