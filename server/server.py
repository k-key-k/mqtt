from mqtt_client import create_mqtt_client
from config import MQTT_TOPIC
import base64
import numpy as np
import cv2
import os
import json

IMAGE_FOLDER = "server/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def on_message(client, userdata, msg):
    print("Image received via MQTT")

    data = json.loads(msg.payload.decode("utf-8"))
    username = data.get("username", "unknown_user")
    image_data = base64.b64decode(data["image"])

    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: Unable to decode image data")
        return

    image_path = os.path.join(IMAGE_FOLDER, f"{username}_received.jpg")
    cv2.imwrite(image_path, image)
    print(f"Image saved to {image_path} from {username}")


mqtt_client = create_mqtt_client("Server")
mqtt_client.on_message = on_message
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_forever()