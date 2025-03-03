import socket

HOST = "0.0.0.0"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))
print("Connected to the server!")
while True:
    msg = input("You: ")
    if msg.lower() == exit:
        break
    client.sendall(msg.encode())
    response = client.recv(1024).decode()
    print(f"Server: {response}")

client.close()
