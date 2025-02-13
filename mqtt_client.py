import paho.mqtt.client as mqtt
from config import MQTT_TOPIC, MQTT_PORT, MQTT_BROKER, USERNAME, PASSWORD

def create_mqtt_client(client_name):
    client = mqtt.Client(client_name)
    client.username_pw_set(USERNAME, PASSWORD)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"{client_name} connected to MQTT Broker!")
        else:
            print(f"{client_name} failed to connect, return code {rc}.")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client