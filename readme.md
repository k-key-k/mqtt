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
4. На устройстве с сервером добавьте правило для подключение по порту 
# Запуск
1. Установите ваш IP в upload_form.html
> 72 fetch('http://0:0:0:0:8000/upload/', {<br>
  73                  method: 'POST',<br>
  74                  body: formData<br>
  75              })
2. Запустите брокер Mosquitto на двух устройствах
> mosquitto
3. Запустите сервер
> python .\server.py
# Структура проекта
>server/ #server <br> 
├── images/             
│   └── received_image.jpg <br>
├── server.py                
├── upload_form.html       
└── requirements.txt       
client/ #client <br>
└── client.py <br>
readme.md
# Использование
- С клиентского устройства перейдите по ссылке: http://**ip**:**port**/
- Загрузите изображение с клиентского устройства
- Изображение сохранится на сервере в папке проекта: .\images\

