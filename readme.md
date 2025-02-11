# MQTT Image Server
# Описание
Приём изображений через HTTP и MQTT в одной WI-FI сети, с сохранением их на сервере.
# Требования 
- Python 3.9
- Mosquitto
# Установка
1. Клонируйте репозиторий
> git clone <ссылка-на-репозиторий>
> cd <путь-к-проекту>
2. Создайте виртуальное окружение
> python -m venv venv
> venv\Scripts\activate
3. Установите зависимости
> pip install -r requirements.txt
# Запуск
1. Запустите брокер Mosquitto
> mosquitto
2. Запустите сервер
> python .\mqtt.py
3. Установите ваш IP в клиентском коде
> MQTT_BROKER = "your_ip"
4. Запустите клиентский код на другом устройстве
> python .\post_mqtt.py
# Структура проекта
>test_mqtt/ #server <br> 
├── images/             
│   └── received_image.jpg <br>
├── mqtt.py                
├── upload_form.html       
└── requirements.txt       
test_post_mqtt/ #client <br>
└── post_mqtt.py <br>
readme.md
# Использование
- Укажите путь к изображению в клиентском коде
- Запустите код
- изображение сохранится на устройстве с сервером в папке test_mqtt/images/

