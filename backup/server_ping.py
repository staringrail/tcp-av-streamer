# server_test.py
import socket

HOST = '0.0.0.0'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SERVER] Listening on port {PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"[SERVER] Connected by {addr}")
