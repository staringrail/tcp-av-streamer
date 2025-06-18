import socket
import threading
import time

# --- Configuration ---
# HOST: Listen on all available network interfaces.
#       This is usually '0.0.0.0' to accept connections from any IP.
HOST = '0.0.0.0'
# PORT: The port your client is trying to connect to (443).
PORT = 443

# --- Function to handle each client connection ---
def handle_client(client_socket, client_address):
    """
    Handles a single client connection. Sends test data and closes the connection.
    """
    print(f"[SERVER] Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        # 1. Send a welcome message
        welcome_message = "Welcome to the test server! You are connected.\n"
        client_socket.sendall(welcome_message.encode('utf-8'))
        print(f"[SERVER] Sent: '{welcome_message.strip()}' to {client_address[0]}")

        # 2. Send a few more messages with a slight delay
        for i in range(1, 4):
            response = f"This is message number {i} from the server.\n"
            client_socket.sendall(response.encode('utf-8'))
            print(f"[SERVER] Sent: '{response.strip()}' to {client_address[0]}")
            time.sleep(1) # Small delay to simulate data transfer over time

        # 3. Wait a moment then signal client to break its loop (by closing server side)
        print(f"[SERVER] All test messages sent to {client_address[0]}. Closing connection after 2 seconds...")
        time.sleep(2) # Give client a moment to receive last message

    except BrokenPipeError:
        print(f"[SERVER] Client {client_address[0]} disconnected unexpectedly (Broken Pipe).")
    except ConnectionResetError:
        print(f"[SERVER] Client {client_address[0]} reset the connection.")
    except socket.timeout:
        print(f"[SERVER] Client {client_address[0]} connection timed out.")
    except Exception as e:
        print(f"[SERVER] Error handling client {client_address[0]}: {e}")
    finally:
        client_socket.close()
        print(f"[SERVER] Connection with {client_address[0]} closed.")

# --- Main server setup ---
def start_server():
    """
    Initializes and starts the server, listening for incoming connections.
    """
    print("[SERVER] Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow reusing the address immediately after closing (prevents 'Address already in use' errors on quick restarts)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # Bind the socket to the host and port
            server_socket.bind((HOST, PORT))
            # Enable the server to accept connections. 5 is the backlog queue size.
            server_socket.listen(5)
            print(f"[SERVER] Listening on {HOST}:{PORT}")
            print(f"[SERVER] Waiting for client connections...")

            while True:
                # Accept an incoming connection
                conn, addr = server_socket.accept()
                # Handle each client in a new thread to allow multiple concurrent clients
                client_handler = threading.Thread(target=handle_client, args=(conn, addr))
                client_handler.start()

        except PermissionError:
            print(f"[SERVER] ERROR: Permission denied. To bind to port {PORT}, you need root/administrator privileges.")
            print("Try running this script with sudo (Linux/macOS) or as Administrator (Windows).")
            print("Example: sudo python3 server_script.py")
        except OSError as e:
            print(f"[SERVER] ERROR: OS Error binding to port {PORT}: {e}")
            if e.errno == 98: # EADDRINUSE (Address already in use)
                print("       Port is likely already in use. Check if another service is using it, or wait a moment.")
            else:
                print(f"       System error number: {e.errno}")
        except KeyboardInterrupt:
            print("\n[SERVER] Server is shutting down gracefully.")
        except Exception as e:
            print(f"[SERVER] An unexpected server error occurred: {e}")

# --- Run the server ---
if __name__ == "__main__":
    start_server()