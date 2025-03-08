import socket
import ssl

class checkers_client:
    def __init__(self, host="localhost", port=5000, certfile="keys/client_certificate.pem", keyfile="keys/client_private_key.pem"):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_server(self):
        self.client_sock.connect((self.host, self.port))
        print(f"connected to server at {self.host}:{self.port}")
    
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile="keys/server_certificate.pem")  # Specify the server's self-signed certificate

        self.client_sock = context.wrap_socket(self.client_sock, server_hostname=self.host)
        print(f"SSL connection established with server.")

    def send_move(self, move):
        if self.client_sock:
            self.client_sock.send(move.encode())
            print(f"client sent move: {move}")
    
    def receive_move(self):
        if self.client_sock:
            try:
                self.client_sock.setblocking(False)
                move = self.client_sock.recv(1024).decode()
                print(f"client recieved move: {move}")
                return move
            except:
                return None
    
    def close(self):
        if self.client_sock:
            self.client_sock.close()
