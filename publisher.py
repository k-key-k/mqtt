import paho.mqtt.client as mqtt
import time

broker = "localhost"
port = 1883
topic = "virtual/device1"


def connect_mqtt():
    client = mqtt.Client("Publisher")
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        message = input("Enter your message to topic: ")
        result = client.publish(topic, message)
        status = result.rc
        if status == mqtt.MQTT_ERR_SUCCESS:
            print(f"Send message {message} into topic {topic}")
        else:
            print(f"Fail to send into the {topic}")
        time.sleep(2)


if __name__ == "__main__":
    client = connect_mqtt()
    publish(client)
