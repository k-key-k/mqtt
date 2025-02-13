import cv2
import os

os.makedirs('webcamera_test/camera_images', exist_ok=True)

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("No access to cam")
    exit()

path = "camera_images/"

ret, frame = capture.read()
if not ret:
    print("No access to camera")
    exit()
cv2.waitKey(10)
cv2.imwrite(f"{path}captured_image.jpg", frame)
image = cv2.imread(f"{path}captured_image.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imwrite(f"{path}captured_image_gray.jpg", image)

capture.release()
