import os
import cv2
import numpy as np
import base64
import json
import paho.mqtt.client as mqtt
import uuid
import subprocess
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, USERNAME, PASSWORD
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
HTML_FILE = os.path.join(BASE_DIR, "upload_form.html")
GALLERY_HTML = os.path.join(BASE_DIR, "gallery.html")
PASSWORD_FILE = os.path.join(BASE_DIR, "../password.txt")

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


@app.get("/images/")
async def get_images():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            images.append({
                "filename": filename,
                "url": f"/images/{filename}"
            })
    return {"images": images}


@app.get("/images/{filename}")
async def get_image(filename: str):
    image_path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


@app.delete("/images/{filename}")
async def delete_image(filename: str):
    image_path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        os.remove(image_path)
        return {"message": f"Image {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {e}")


@app.get("/gallery/", response_class=FileResponse)
async def get_gallery():
    return FileResponse(GALLERY_HTML)


class RegisterRequest(BaseModel):
    username: str
    password: str
@app.post("/register/")
async def register_client(request: RegisterRequest):
    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    if not os.path.exists(PASSWORD_FILE):
        open(PASSWORD_FILE, "w").close()

    try:
        subprocess.run(
            ["mosquitto_passwd", "-b", PASSWORD_FILE, username, password],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return {"message": "Client registered successfully"}
    except subprocess.CalledProcessError as e:
        if "already exists" in e.stderr.decode():
            raise HTTPException(status_code=400, detail="Username already exists")
        raise HTTPException(status_code=500, detail="Failed to register client")


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

    filename = generate_unique_filename(file.filename)
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


def compress_image(image, quality=60):
    _, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return buffer.tobytes()


def generate_unique_filename(original_filename=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    if original_filename:
        name, ext = os.path.splitext(original_filename)
        return f"{name}_{timestamp}_{unique_id}{ext}"
    return f"image_{timestamp}_{unique_id}.jpg"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
