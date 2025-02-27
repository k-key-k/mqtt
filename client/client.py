from mqtt_client import create_mqtt_client
from config import MQTT_TOPIC, USERNAME
import paho.mqtt.client as mqtt
import base64
import time
import json
import cv2
import logging

IMAGE_PATH = "client/test.jpg"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def compress_image(image, quality=60):
    _, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return buffer.tobytes()


def send_image_mqtt(image_data):
    try:
        mqtt_client = create_mqtt_client("Client")
        mqtt_client.loop_start()
        time.sleep(1)

        payload = json.dumps({
            "username": USERNAME,
            "image": image_data
        })

        mqtt_client.publish(MQTT_TOPIC, payload)
        logging.info(f"Image sent via MQTT from {USERNAME}")

        mqtt_client.loop_stop()
        mqtt_client.disconnect()

    except Exception as e:
        logging.info(f"Error sending image: {e}")


def send_image():
    try:
        with open(IMAGE_PATH, "rb") as img_file:
            image = cv2.imread(IMAGE_PATH)
            if image is None:
                print("Error: Unable to read image file")
                return

            compressed_image = compress_image(image, quality=60)
            image_data = base64.b64encode(compressed_image).decode()
            send_image_mqtt(image_data)
    except Exception as e:
        print(f"Error reading image file: {e}")


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

    compressed_image = compress_image(frame, quality=85)
    image_data = base64.b64encode(compressed_image).decode()
    send_image_mqtt(image_data)


if __name__ == "__main__":
    mode = input("Choose sent method (1 - file, 2 - cam): ").strip()
    if mode == "1":
        send_image()
    elif mode == "2":
        camera_sent_image()
    else:
        print("Incorrect input. Exit.")
