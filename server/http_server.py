import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
HTML_FILE = os.path.join(BASE_DIR, "../upload_form.html")

os.makedirs(IMAGE_FOLDER, exist_ok=True)

app = FastAPI()


@app.get("/", response_class=FileResponse)
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
