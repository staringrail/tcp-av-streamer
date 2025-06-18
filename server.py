import socket

HOST = '0.0.0.0' # Accept connections on all interfaces
PORT = 443       # Use port 443 (firewall-friendly)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[SERVER] Listening on port {PORT}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"[SERVER] Connnected by {addr}")
        while True:
            message = input("Enter message to send: ")
            conn.sendall(message.encode('utf-8'))