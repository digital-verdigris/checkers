import socket
import threading
import json

class checkers_server:
    def __init__(self, host = "0.0.0.0", port = 5000):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = None
        self.client_addr = None
    
    def start_listener(self):
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)
        print(f"waiting for a client to connect on {self.host}:{self.port}...")
        self.client_sock, self.client_addr = self.server_sock.accept()
        print(f"client {self.client_addr} connected!")
    
    def send_move(self, move):
        if self.client_sock:
            self.client_sock.sendall(move.encode())
            print(f"server sent move: {move}")

    def receive_move(self):
        if self.client_sock:
            try:
                self.client_sock.setblocking(False)
                move = self.client_sock.recv(1024).decode()
                print(f"server recieved move: {move}")
                return move
            except:
                return None
        return None

    def wait_for_client(self, menu, window):
        while self.client_sock is None:
            if not menu.draw_waiting_for_connection(window):
                break
            pass
        return True
    
    def close(self):
        if self.client_sock:
            self.client_sock.close()
        self.server_sock.close()