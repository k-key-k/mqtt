import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "microscope/image")
USERNAME = os.getenv("MQTT_USERNAME", "username")
PASSWORD = os.getenv("MQTT_PASSWORD", "password")
SECRET_KEY = os.getenv("SECRET_KEY", "random_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
