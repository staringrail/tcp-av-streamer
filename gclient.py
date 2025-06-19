import socket
import cv2
import pickle
import struct
import zlib
import sys

# Define server address and port
# This should match the server's host and port
SERVER_HOST = '192.168.68.52' # Use '127.0.0.1' for localhost, or the server's IP address
SERVER_PORT = 9999

def start_client():
    """
    Connects to the webcam streaming server, receives compressed frames,
    decompresses, decodes, and displays them.
    """
    client_socket = None
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server.")

        data_buffer = b""
        payload_size = struct.calcsize("<I") # Size of the unsigned integer for message length

        while True:
            # Continuously receive data until the full message size is received
            while len(data_buffer) < payload_size:
                packet = client_socket.recv(4096) # Receive data in chunks
                if not packet:
                    print("No more data received from server. Server might have closed the connection.")
                    break # Exit if no data is received (connection closed)
                data_buffer += packet

            if not packet: # Break if connection was closed
                break

            # Extract the message size from the buffer
            packed_msg_size = data_buffer[:payload_size]
            data_buffer = data_buffer[payload_size:]
            msg_size = struct.unpack("<I", packed_msg_size)[0]

            # Receive the actual frame data based on the extracted size
            while len(data_buffer) < msg_size:
                data_buffer += client_socket.recv(4096) # Keep receiving until full frame received

            # Extract the compressed frame data
            compressed_frame_data = data_buffer[:msg_size]
            data_buffer = data_buffer[msg_size:]

            # Decompress the frame data
            try:
                decompressed_frame_data = zlib.decompress(compressed_frame_data)
            except zlib.error as ze:
                print(f"Zlib decompression error: {ze}. Skipping frame.")
                continue # Skip this frame and try for the next

            # Convert bytes to a numpy array (image)
            # Use np.frombuffer to create a numpy array from the byte data
            # Use cv2.imdecode to decode the JPEG image
            nparr = cv2.imdecode(cv2.IMREAD_UNCHANGED, cv2.IMALL_PNG, decompressed_frame_data)
            if nparr is None:
                print("Failed to decode image from received data. Skipping frame.")
                continue

            # Display the frame
            cv2.imshow('Webcam Stream', nparr)

            # Wait for 1 millisecond and check for 'q' key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except ConnectionRefusedError:
        print(f"Error: Connection refused. Make sure the server is running on {SERVER_HOST}:{SERVER_PORT}.")
    except socket.error as se:
        print(f"Socket error: {se}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up resources
        if client_socket:
            client_socket.close()
        cv2.destroyAllWindows() # Close all OpenCV windows
        print("Client stopped.")

if __name__ == "__main__":
    start_client()
