from mqtt_client import create_mqtt_client
from config import MQTT_TOPIC, USERNAME
import paho.mqtt.client as mqtt
import base64
import time
import json

IMAGE_PATH = "client/test.jpg"


def send_image():
    try:
        with open(IMAGE_PATH, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode()

        mqtt_client = create_mqtt_client("Client")
        mqtt_client.loop_start()
        time.sleep(1)

        payload = json.dumps({
            "username": USERNAME,
            "image": image_data
        })

        mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"Image sent via MQTT from {USERNAME}")

        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    except Exception as e:
        print(f"Error sending image: {e}")


if __name__ == "__main__":
    send_image()
