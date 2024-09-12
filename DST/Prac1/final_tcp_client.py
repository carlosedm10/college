# Constants for the server's address and port
import base64
import socket
import pyotp
from constants import DNI

SERVER_ADDRESS = "158.42.32.220"
SERVER_PORT = 21000
server_responded = False

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using the specified address and port
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Generate TOTP secret using the DNI
secret = base64.b32encode(bytearray(DNI, "ascii")).decode("utf-8")
totp_object = pyotp.TOTP(secret)
qr_text = totp_object.provisioning_uri(name="mi_usuario", issuer_name="Mi App")

# Prepare the message
message = f"Carlos Eduardo Dominguez Martinez#{DNI}#"

# Encode the message into bytes before sending it
client_socket.send(message.encode("utf-8"))

# Wait for the server to respond
while not server_responded:
    # Receive the message from the server (up to 1024 bytes)
    received_message = client_socket.recv(1024)

    # Decode and print the received message
    print(received_message.decode("utf-8"))

    # If a message was received, mark server_responded as True
    if received_message:
        server_responded = True

# End the connection to the server
client_socket.close()