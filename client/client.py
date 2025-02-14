from mqtt_client import create_mqtt_client
from config import MQTT_TOPIC, USERNAME
import paho.mqtt.client as mqtt
import base64
import time
import json
import cv2

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

def camera_sent_image():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("No access to cam")
        return
    ret, frame = capture.read()
    capture.release()
    if not ret:
        print("No access to camera")
        return

    _, buffer = cv2.imencode(".jpg", frame)
    image_data = base64.b64encode(buffer).decode()

    try:
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
    mode = input("Choose sent method (1 - file, 2 - cam): ").strip()
    if mode == 1:
        send_image()
    elif mode == 2:
        camera_sent_image()
    else:
        print("Incorrect input. Exit.")
