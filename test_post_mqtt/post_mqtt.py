import paho.mqtt.client as mqtt
import base64
import time
from PIL import Image
from io import BytesIO

broker_ip = "94.180.169.106"
port = 1883
topic = "image_topic"

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

client = mqtt.Client()
client.connect(broker_ip, port, 60)

client.loop_start()

image_path = "path_to_your_image.png"
base64_image = image_to_base64(image_path)

client.publish(topic, base64_image)
print("Image sent!")

time.sleep(2)
client.loop_stop()
client.disconnect()
