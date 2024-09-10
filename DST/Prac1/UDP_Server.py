import socket

UDP_ADDRESS = "127.0.0.1"
UDP_PORT = 15002
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(
    (UDP_ADDRESS, UDP_PORT)
)  # associates the IP address and port number to the server.
print("Server's Up and Running")
message, client_address = server_sock.recvfrom(2048)  # 2048 is the buffer size
print("message Recieved:", message.decode())
server_sock.close()
