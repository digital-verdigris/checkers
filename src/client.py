import socket

class checkers_client:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        print(f"connected to server at {self.host}:{self.port}")
    
    def send_move(self, move):
        if self.client_socket:
            self.client_socket.send(move.encode())
            print(f"client sent move: {move}")
    
    def receive_move(self):
        if self.client_socket:
            try:
                move = self.client_socket.recv(1024).decode()
                print(f"client recieved move: {move}")
                return move
            except:
                return None
    
    def close(self):
        if self.client_socket:
            self.client_socket.close()
