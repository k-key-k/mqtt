import os
import cv2
import numpy as np
import base64
import json
import paho.mqtt.client as mqtt
import uuid
from datetime import datetime, timedelta
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, USERNAME, PASSWORD, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
HTML_FILE = os.path.join(BASE_DIR, "upload_form.html")
GALLERY_HTML = os.path.join(BASE_DIR, "gallery.html")
USERS_DB_FILE = os.path.join(BASE_DIR, "users.json")

os.makedirs(IMAGE_FOLDER, exist_ok=True)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


app = FastAPI()

mqtt_client = mqtt.Client("HTTP_Server")
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()


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


def load_users():
    if not os.path.exists(USERS_DB_FILE):
        return {"users": []}
    with open(USERS_DB_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    users = load_users()
    for user in users["users"]:
        if user["username"] == username:
            return UserInDB(username=user["username"], hashed_password=user["hashed_password"])
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/", response_class=FileResponse)
async def get_upload_form():
    return FileResponse(HTML_FILE)


@app.get("/config/")
async def get_config():
    return {"server_ip": MQTT_BROKER}


@app.post("/register/", response_model=User)
async def register_user(user: User):
    users = load_users()
    if any(u["username"] == user.username for u in users["users"]):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    users["users"].append({"username": user.username, "hashed_password": hashed_password})
    save_users(users)
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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


@app.post("/upload/")
async def upload_image(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
):
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

        payload = json.dumps({"username": current_user.username, "image": image_data})
        mqtt_client.publish(MQTT_TOPIC, payload)

        print(f"Image published to MQTT topic {MQTT_TOPIC}")
        return {"message": "Image received and published to MQTT", "filename": filename}

    except Exception as e:
        print(f"Error publishing to MQTT: {e}")
        return {"error": "Failed to publish image to MQTT"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
