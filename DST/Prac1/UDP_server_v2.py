import socket

UDP_ADDRESS = "127.0.0.1"
UDP_PORT = 16000
communication_active = True

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((UDP_ADDRESS, UDP_PORT))
print("Server's Up and Running")

while communication_active:
    message, client_address = server_sock.recvfrom(2048)
    print("(Server) Message recieved: ", message.decode(), "sending...")

    modified_message = message.decode().upper()  # Transforms to uppercase
    server_sock.sendto(
        modified_message.encode(), client_address
    )  # Sends the message to the client

    server_message = input("(Server) Write 'end' to finish the transmission: ")
    server_sock.sendto(server_message.encode(), client_address)
    if server_message.lower() == "end":
        communication_active = False
        print("(Server) Transmission Finished.")
        break

server_sock.close()
