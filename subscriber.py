import paho.mqtt.client as mqtt
import threading

broker = "localhost"
port = 1883
topic = "virtual/device1"

# Callback при получении сообщения
def on_message(client, userdata, message):
    print(f"Subscriber {userdata} received message: {message.payload.decode()} from topic: {message.topic}")

def connect_mqtt(client_name):
    client = mqtt.Client(client_name)
    client.on_message = on_message
    client.user_data_set(client_name)  # Устанавливаем имя подписчика как userdata
    client.connect(broker, port)
    client.subscribe(topic)
    return client

def subscribe(client):
    client.loop_forever()  # Запуск бесконечного цикла получения сообщений

def start_subscriber(client_name):
    client = connect_mqtt(client_name)
    # Запускаем подписку в отдельном потоке
    subscriber_thread = threading.Thread(target=subscribe, args=(client,))
    subscriber_thread.start()

if __name__ == "__main__":
    # Запуск нескольких подписчиков
    start_subscriber("Subscriber_1")
    start_subscriber("Subscriber_2")
    start_subscriber("Subscriber_3")
