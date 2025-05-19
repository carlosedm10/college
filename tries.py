# udp_bridge.py
import socket
import threading
import time

RASPBERRY_IP = "10.42.0.150"
RASPBERRY_PORT = 5004
MAC_IP = "127.0.0.1"
DOCKER_PORT = 5005

sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_in.bind((RASPBERRY_IP, RASPBERRY_PORT))

sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_docker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(
    f"Escuchando en {RASPBERRY_IP}:{RASPBERRY_PORT} y reenviando a {MAC_IP}:{DOCKER_PORT}"
)


def forward_to_docker():
    while True:
        data, _ = sock_in.recvfrom(1024)
        print(f"\nRecibido de  Raspberry Pi, data: {data}")
        sock_out.sendto(data, (MAC_IP, DOCKER_PORT))
        print(f"Enviando al Docker {MAC_IP}:{DOCKER_PORT}")
        time.sleep(1)


def forward_from_docker():
    while True:
        data, _ = sock_docker.recvfrom(1024)
        print(f"\nRecibido de Docker, data: {data}")
        sock_out.sendto(data, (RASPBERRY_IP, RASPBERRY_PORT))
        print(f"Enviando a la Raspberry Pi {RASPBERRY_IP}:{RASPBERRY_PORT}")
        time.sleep(1)


# Start both forwarding threads
thread1 = threading.Thread(target=forward_to_docker)
thread2 = threading.Thread(target=forward_from_docker)

thread1.start()
thread2.start()

# Keep main thread alive
while True:
    time.sleep(1)
