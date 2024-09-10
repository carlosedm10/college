import socket

UDP_ADDRESS = "127.0.0.1"
UDP_PORT = 15002
message = input("Introduce a message: ")
client_sock = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM  # socket type to use for UDP
)
client_sock.sendto(
    message.encode(),  # end code transforms to bites.
    (UDP_ADDRESS, UDP_PORT),
)  # UDP doesn't check for connection, it just sends the data.


client_sock.close()
