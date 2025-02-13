from mqtt.mqtt_client import create_mqtt_client
from mqtt.config import MQTT_TOPIC
import paho.mqtt.client as mqtt
import base64

IMAGE_PATH = "test.jpg"

def send_image():
    try:
        with open(IMAGE_PATH, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode()

        mqtt_client = create_mqtt_client("Client")
        mqtt_client.loop_start()
        mqtt_client.sleep(1)

        mqtt_client.publish(MQTT_TOPIC, image_data)
        print("Image sent via MQTT")

        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    except Exception as e:
        print(f"Error sending image: {e}")

if __name__ == "__main__":
    send_image()