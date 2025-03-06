import socket
import threading
import json

class checkers_server:
    def __init__(self, port = 5000):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_conn = None
        self.move_queue = []

    def start_listener(self):
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(1)
        print(f"listening for connection on port {self.port}...")

        conn, addr = self.sock.accept()
        print(f"Connected to peer: {addr}")
        self.peer_conn = conn

        threading.Thread(target=self.receive_moves, args=(conn,), daemon=True).start()

    def receive_moves(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                move = json.loads(data)
                print(f"received move: {move}")
                self.move_queue.append(move)
            except:
                break

    def send_move(self, move):
        if self.peer_conn:
            move_data = {"move": move}
            self.peer_conn.sendall(json.dumps(move_data).encode())
            print(f"sent move: {move}")

    def close_connection(self):
        if self.peer_conn:
            self.peer_conn.close()
        self.sock.close()