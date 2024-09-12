"""
TCP is oriented to connections, we can send and receive messages in both directions
"""

import socket


# Constants for the server's address and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 19000

# Create a TCP/IP socket, once created, the socket is ready to be used
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

print("Server's Up and Running")

server_socket.listen(5)  # Max number of connections to queue

while True:
    # No need to check for IP address and port, it is already bound.
    # Accept a new connection
    client_socket, addr = server_socket.accept()
    print(f"Connection established from {addr}!")

    # Send a welcome message to the client
    client_socket.send(bytes("Welcome to the Server", "utf-8"))

    # Close the client socket after sending the message
    client_socket.close()
