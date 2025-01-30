import os
import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt
from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

# Настройки MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "microscope/image"

# Папка для сохранения изображений
IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)  # Создаем папку, если она не существует


# Функция обработки сообщений MQTT
def on_message(client, userdata, msg):
    print("Image from MQTT")
    image_data = base64.b64decode(msg.payload)
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Сохраняем изображение в папку
    image_path = os.path.join(IMAGE_FOLDER, "received_image_mqtt.jpg")
    cv2.imwrite(image_path, image)
    print(f"Image saved to {image_path}")


# Настройка клиента MQTT
mqtt_client = mqtt.Client("ImageReceiver")
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()


@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image = await file.read()
    np_img = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Сохраняем изображение в папку
    image_path = os.path.join(IMAGE_FOLDER, "received_http_image.jpg")
    cv2.imwrite(image_path, img)
    print(f"Image saved to {image_path}")
    return {"message": "Image received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
