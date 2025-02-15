import os
import cv2
import numpy as np
import base64
import json
import paho.mqtt.client as mqtt
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, USERNAME, PASSWORD

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
HTML_FILE = os.path.join(BASE_DIR, "../upload_form.html")

os.makedirs(IMAGE_FOLDER, exist_ok=True)

app = FastAPI()

mqtt_client = mqtt.Client("HTTP_Server")
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()


@app.get("/", response_class=FileResponse)
async def get_upload_form():
    return FileResponse(HTML_FILE)


@app.get("/config/")
async def get_config():
    return {"server_ip": MQTT_BROKER}


def compress_image(image, quality=60):
    _, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return buffer.tobytes()


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG images are allowed")

    image = await file.read()
    np_img = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image format"}

    compressed_image = compress_image(img, quality=60)
    img = cv2.imdecode(np.frombuffer(compressed_image, np.uint8), cv2.IMREAD_COLOR)

    filename = f"received_{file.filename}" if file.filename else "received_http_image.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)
    cv2.imwrite(image_path, img)

    print(f"Image saved to {image_path}")

    try:
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode()

        payload = json.dumps({"username": USERNAME, "image": image_data})
        mqtt_client.publish(MQTT_TOPIC, payload)

        print(f"Image published to MQTT topic {MQTT_TOPIC}")
        return {"message": "Image received and published to MQTT", "filename": filename}

    except Exception as e:
        print(f"Error publishing to MQTT: {e}")
        return {"error": "Failed to publish image to MQTT"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
