import socket

UDP_ADDRESS = "127.0.0.1"
UDP_PORT = 16000
communication_active = True

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while communication_active:
    message = input("(Client) Introduce a message to send: ")
    client_sock.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))

    modified_message, server_address = client_sock.recvfrom(2048)
    print("(Client) Response from server :", modified_message.decode())

    if message.lower() == "end" or modified_message.decode() == "END":
        communication_active = False
        print("(Client) Finished Transmision.")
        break

client_sock.close()
