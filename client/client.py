import paho.mqtt.client as mqtt
import base64
import time
import cv2

MQTT_BROKER = "your_ip"
MQTT_PORT = 1884
MQTT_TOPIC = "microscope/image"

def image_to_base64(image_path):
    image = cv2.imread(image_path)
    _, buffer = cv2.imencode('.jpg', image)
    image_data = base64.b64encode(buffer).decode('utf-8')
    return image_data

def send_image(client, image_path):
    base64_image = image_to_base64(image_path)
    client.publish(MQTT_TOPIC, base64_image)
    print("Image sent to MQTT broker")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

try:
    image_path = "test_image.jpg"  # Укажите путь к вашему изображению

    while True:
        send_image(client, image_path)
        time.sleep(5)
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    client.loop_stop()
    client.disconnect()
