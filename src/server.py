import socket
import threading

HOST = "0.0.0.0"

def receive_msgs(conn):
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"\nPeer: {msg}\nYou: ", end="")
        except:
            break
    conn.close()

def send_msgs(conn):
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            conn.close()
            break
        conn.sendall(msg.encode())

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(1)
    print(f"Listening for incoming connections on port {port}...")

    conn, addr = server.accept()
    print(f"Connected to {addr}")

    threading.Thread(target=receive_msgs, args=(conn,), daemon=True).start()
    threading.Thread(target=send_msgs, args=(conn,), daemon=True).start()

def connect_to_peer(peer_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, port))
    print(f"Connected to peer at {peer_ip}:{port}")

    threading.Thread(target=receive_msgs, args=(client,), daemon=True).start()
    threading.Thread(target=send_msgs, args=(client,), daemon=True).start()
    
if __name__ == "__main__":
    peer_ip = input("Enter peer's IP to connect (or press Enter to wait for connection only): ").strip()
    
    if peer_ip:
        connect_to_peer(peer_ip, 5001)
    else:
        start_server(5000)