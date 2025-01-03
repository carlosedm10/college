import os
import paho.mqtt.client as mqtt
from environs import Env
import time


BROKER_IP = "158.42.32.220"
PORT = 1883

PETICION = "DST/PETICION"
CODIGO = "DST/CODIGO"
SOLUCION = "DST/SOLUCION"

env = Env()
env.read_env()
DNI = os.getenv("DNI")
NAME = "Carlos Eduardo"
UPV_USERNAME = os.getenv("UPV_USERNAME")


def on_message(client: mqtt.Client, _, message: mqtt.MQTTMessage):
    response = str(message.payload.decode("utf-8"))

    print("Mensaje recibido: ", response)
    solution = f"{response};{NAME};{UPV_USERNAME}"
    # Sending the response
    client.publish(SOLUCION, solution)
    client.disconnect()
    client.loop_stop()


# Sending th DNI
cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.username_pw_set(username="dst", password="dst")
cliente.connect(BROKER_IP, PORT)
print("conectado al Broker: ", BROKER_IP)

cliente.publish(PETICION, DNI)
print("publicado el mensaje: ", DNI, " en el topic: ", PETICION)

# Subscribing to the topic where the broker will send the code
cliente.subscribe(CODIGO)
cliente.on_message = on_message


cliente.loop_forever()
