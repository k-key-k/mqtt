import os
import cv2
import numpy as np
import base64
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as mqtt
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "upload_form.html")
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")

MQTT_BROKER = "localhost"
MQTT_PORT = 1884
MQTT_TOPIC = "microscope/image"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

def on_message(client, userdata, msg):
    print("Image from MQTT")
    image_data = base64.b64decode(msg.payload)
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: Unable to decode image data")
        return

    print(f"Received image size: {image.shape}")

    image_path = os.path.join(IMAGE_FOLDER, "received_mqtt_image.jpg")
    if cv2.imwrite(image_path, image):
        print(f"Image saved to {image_path}")
    else:
        print("Failed to save image")

mqtt_client = mqtt.Client("ImageReceiver")
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    return FileResponse(HTML_FILE)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image = await file.read()
    np_img = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    filename = f"received_{file.filename}" if file.filename else "received_http_image.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)

    cv2.imwrite(image_path, img)
    print(f"Image saved to {image_path}")
    return {"message": "Image received", "filename": filename}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)