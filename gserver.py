import socket
import cv2
import pickle
import struct
import zlib
import sys

# Define server address and port
# Use '0.0.0.0' to listen on all available network interfaces
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

def start_server():
    """
    Initializes and starts the webcam streaming server.
    Captures video from the webcam, compresses frames, and sends them to connected clients.
    """
    server_socket = None
    try:
        # Create a socket object
        # AF_INET specifies the address family (IPv4)
        # SOCK_STREAM specifies the socket type (TCP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow reuse of the address to prevent "Address already in use" errors
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the host and port
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        # Listen for incoming connections (max 5 queued connections)
        server_socket.listen(5)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        # Initialize video capture from the default webcam (0)
        # Change 0 to a different index if you have multiple cameras
        cap = cv2.VideoCapture(0)

        # Check if the webcam was opened successfully
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        print("Waiting for client connection...")
        conn, addr = server_socket.accept()
        print(f"Client connected from: {addr}")

        # Loop to capture and send frames
        while True:
            ret, frame = cap.read() # Read a frame from the webcam
            if not ret:
                print("Failed to grab frame, exiting...")
                break

            # Encode the frame as JPEG to reduce size
            # This returns (boolean, buffer) where buffer is the JPEG compressed image
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] # JPEG quality 90%
            result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)

            if not result:
                print("Failed to encode frame.")
                continue

            # Convert the encoded frame to bytes
            data = encoded_frame.tobytes()

            # Compress the data using zlib
            compressed_data = zlib.compress(data, level=9) # level 9 for max compression

            # Pack the size of the compressed data into a 4-byte little-endian struct
            # 'I' for unsigned int, '<' for little-endian
            msg_size = struct.pack("<I", len(compressed_data))

            try:
                # Send the size of the compressed data first
                conn.sendall(msg_size)
                # Send the compressed data
                conn.sendall(compressed_data)
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Client disconnected: {e}")
                break # Break out of the loop if client disconnects
            except Exception as e:
                print(f"Error sending data: {e}")
                break

    except socket.error as se:
        print(f"Socket error: {se}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up resources
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        if server_socket:
            server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    start_server()
