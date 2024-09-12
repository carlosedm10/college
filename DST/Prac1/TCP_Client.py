import socket

# Constants for the server's address and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 19000

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using the specified address and port
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Receive the message from the server (up to 1024 bytes)
received_message = client_socket.recv(1024)

# Decode and print the received message
print(received_message.decode())

# Close the connection to the server
client_socket.close()
