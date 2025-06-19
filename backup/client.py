import socket

# Change this to your server's LAN IP
SERVER_IP = '192.168.68.65'  # Replace with your actual server IP
PORT = 443

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, PORT))
        print(f"[CLIENT] Connected to server at {SERVER_IP}:{PORT}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("[CLIENT] Received:", data.decode('utf-8'))

except ConnectionRefusedError:
    print("[ERROR] Connection refused. Is the server running and reachable?")
except OSError as e:
    print(f"[ERROR] OS error: {e}")
