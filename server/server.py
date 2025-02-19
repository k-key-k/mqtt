from paho.mqtt import client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, USERNAME, PASSWORD
import base64
import numpy as np
import cv2
import os
import json

IMAGE_FOLDER = "server/process_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def on_message(client, userdata, msg):
    print("Image received via MQTT")

    data = json.loads(msg.payload.decode("utf-8"))
    username = data.get("username", "unknown_user")
    image_data = base64.b64decode(data["image"])
    original_filename = data.get("filename", "image")

    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: Unable to decode image data")
        return

    # Обработка изображения (AI -> Fuzzifier -> Expert System -> Defuzzifier -> Aggregator)
    processed_image = process_image(image)

    # Сохранение обработанного изображения
    processed_image_path = os.path.join(IMAGE_FOLDER, original_filename)
    cv2.imwrite(processed_image_path, processed_image)
    print(f"Processed image saved to {processed_image_path}")

    # Отправка результата обратно в HTTP-сервер
    with open(processed_image_path, "rb") as img_file:
        processed_image_data = base64.b64encode(img_file.read()).decode()

    payload = json.dumps({"username": username, "image": processed_image_data, "filename": original_filename})
    client.publish("processed/image", payload)
    print(f"Processed image published to MQTT topic 'processed/image'")


def process_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


# Создание MQTT-клиента
mqtt_client = mqtt.Client("Server")
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.on_message = on_message
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_forever()