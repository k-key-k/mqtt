from mqtt.mqtt_client import create_mqtt_client
from mqtt.config import MQTT_TOPIC
import base64
import numpy as np
import cv2
import os

IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def on_message(client, userdata, msg):
    print("Image received via MQTT")

    image_data = base64.b64decode(msg.payload)
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: Unable to decode image data")
        return

    image_path = os.path.join(IMAGE_FOLDER, "received_mqtt_image.jpg")
    cv2.imwrite(image_path, image)
    print(f"Image saved to {image_path}")


mqtt_client = create_mqtt_client("Server")
mqtt_client.on_message = on_message
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_forever()