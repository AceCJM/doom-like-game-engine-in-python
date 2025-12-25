class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        import socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = []
    
    def accept_clients(self):
        import threading
        def handle_client(client_socket):
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message:
                        print(f"Received: {message}")
                        self.broadcast(message, client_socket)
                    else:
                        break
                except:
                    break
            client_socket.close()
            self.clients.remove(client_socket)
        
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    
    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)
class Client:
    def __init__(self, server_ip='127.0.0.1', server_port=5555):
        import socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")
    
    def send_message(self, message):
        self.client.send(message.encode('utf-8'))
    
    def receive_messages(self):
        import threading
        def listen():
            while True:
                try:
                    message = self.client.recv(1024).decode('utf-8')
                    if message:
                        print(f"Received: {message}")
                    else:
                        break
                except:
                    break
            self.client.close()
        
        listener_thread = threading.Thread(target=listen)
        listener_thread.start()

    # Game Engine methods
    def send_player_position(self, position):
        message = f"POSITION:{position[0]},{position[1]},{position[2]}"
        self.send_message(message)
    
    def receive_player_positions(self):
        # This method would parse incoming messages for player positions
        def parse_position_message(message):
            if message.startswith("POSITION:"):
                _, coords = message.split(":", 1)
                x, y, z = map(float, coords.split(","))
                return (x, y, z)
            return None

        self.receive_messages()