import socket
import threading
import time

# Define server address and port
server_address = '172.22.0.2'
server_port = 6000

# Function to send a write command
def send_write_command(client_socket, message):
    client_socket.sendall(message.encode())
    print(f"Sent: {message}")

# Function to send a read command
def send_read_command(client_socket):
    client_socket.sendall("read".encode())
    print("Sent: read")

# Create a TCP client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((server_address, server_port))
    print(f"Connected to {server_address}:{server_port}")
    
    # Example to send 2 write commands at the same time
    write_command1 = "write: This is the first sample line to write into the file."
    write_command2 = "write: This is the second sample line to write into the file."
    
    # Start two threads for concurrent write requests
    thread1 = threading.Thread(target=send_write_command, args=(client_socket, write_command1))
    thread2 = threading.Thread(target=send_write_command, args=(client_socket, write_command2))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Send a read command after the write commands
    send_read_command(client_socket)
    
    # Optional: You can add more write/read requests in the loop as needed.
    time.sleep(1)
