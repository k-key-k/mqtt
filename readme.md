# MQTT Image Server
# Описание
Приём изображений через HTTP и MQTT в одной WI-FI сети, с сохранением их на сервере.


# Требования 
- Python 3.9
- Mosquitto


# Установка Mosquitto и Python 3.9
1. Установите архив с Python 3.9, если он не установлен с [официального сайта](https://www.python.org/downloads/release/python-3913/)
2. Установите Mosquitto с [официального сайта](https://mosquitto.org/download/)


# Настройка проекта на Python 3.9 (Командная строка)
1. Клонируйте репозиторий и перейдите в него:
```bash
git clone https://github.com/k-key-k/mqtt.git
cd mqtt
```
2. Для того чтобы использовать нужную версию Python в проекте, создайте виртуальное окружение с версией Python 3.9:
   1. Откройте терминал (или командную строку) и перейдите в директорию вашего проекта.
   2. Создайте виртуальное окружение, указывая путь к Python 3.9: 
   ```bash
   python3.9 -m venv venv39
   ```
   Если команда `python3.9` не работает, укажите полный путь до интерпретатора Python 3.9.
   ```bash
   C:\path\to\python3.9\python.exe -m venv venv39
   ```
   3. Активируйте виртуальное окружение:
   ```bash
   .\venv39\Scripts\activate
   ```
   4. Установите все зависимости проекта, указанные в файле `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
# Настройка проекта на Python 3.9 (PyCharm)
1. Клонируйте репозиторий:
```bash
git clone https://github.com/k-key-k/mqtt.git
```
2. Настройка виртуального окружения в PyCharm:
   1. Перейдите в меню `File` → `Settings` → `Project: <project_name>` → `Python Interpreter`.
   2. Нажмите на иконку шестерёнки в правом верхнем углу и выберите `Add...`.
   3. В открывшемся окне выберите `New environment`.
   4. Нажмите на значок папки и укажите путь к интерпретатору Python в созданном виртуальном окружении:
   ```bash
   <path_to_project>\venv39\Scripts\python.exe
   ```
   5. Нажмите ОК для сохранения настроек.<br><br>
3. Активируйте виртуальное окружение:
   ```bash
   .\venv39\Scripts\activate
   ```

4. Установите все зависимости проекта, указанные в файле `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
# Настройка сервера
1. Настройте правило для подключений к порту (например по 8000) в Windows Брандмауэре:<br>
   1. `Брандмауэр Защитника Windows` -> `Дополнительные параметры` -> `Правила для входящих подключений` -> `Создать правило`
   <br> **Данный пункт настройки можно пропустить, если сервер и клиент запускаются на одном устройстве**

[//]: # (2. Перейдите в директорию с `Mosquitto` и создайте файл паролей:)

[//]: # (```bash)

[//]: # (cd "path\to\mosquitto")

[//]: # (mosquitto_passwd -c passwd your_username)

[//]: # (```)

[//]: # (Введите пароль и подтвердите его)
[//]: # (3. Если нужно создать еще одного пользователя &#40;необязательно&#41;:)

[//]: # (```bash)

[//]: # (mosquitto_passwd passwd another_user)

[//]: # (```)
2. В конфигурационный файл `mosquitto.conf` добавьте следующие строки:
```bash
listener <free_port>
allow_anonymous false
password_file path\to\project\passwords.txt
```
`free_port` - любой доступный порт который сейчас не занят другими службами/программами. Проверить доступность порта можно через командную строку:
```bash
netstat -a | findstr <your_port>
```
3. Добавьте первого пользователя в `passwords.txt`, который уже находится в директории проекта:
```bash
mosquitto_passwd -b passwords.txt username password
```
4. Задайте ваши данные в `config.py`:
```bash
MQTT_BROKER = "localhost" # ваш IP
MQTT_PORT = "your_port" # как в mosquitto.conf
MQTT_TOPIC = "microscope/image" 
USERNAME = "username" # имя пользователя созданного в пунктах 2-3
PASSWORD = "password" # пароль пользователя созданного в пунктах 2-3
SECRET_KEY = "random_key" # случайное число в формате str
ALGORITHM = "HS256" # случайный алгоритм хэширования
```
5. Запустите брокер Mosquitto с конфигурационным файлом через командную строку:
```bash
"C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf" -v
```
6. Запустите MQTT сервер:
```bash
python -m server.server
```
7. Запустите HTTP сервер:
```bash
python -m server.http_server
```
# Настройка устройства для подключения к сети MQTT
1. Перейдите в директорию с установленным Mosquitto `path/to/mosquitto/`
2. В конфигурационный файл `mosquitto.conf` добавьте следующие строки:
```bash
listener <server_port>
```
`server_port` - порт на котором сейчас работает сервер<br>
3. Настройте config.py:
```bash
MQTT_BROKER = "localhost" # IP сервера
MQTT_PORT = "your_port" # Порт сервера
MQTT_TOPIC = "microscope/image" 
USERNAME = "username" # Имя пользователя (должен быть авторизован сервером)
PASSWORD = "password" # Пароль
```
4. Запустите брокер Mosquitto с конфигурационным файлом через командную строку:
```bash
"C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf" -v
```
5. Запустите `client.py` для отправки MQTT запроса:
```bash
python -m client.client
```
Появиться окно с выбором метода отправки:
```bash
Choose sent method (1 - file, 2 - cam):
```
Отправленное изображение сохраниться в `server/images` с `username` отправителя. 
# Работа HTTP запросов
1. Если сервер развернут, то находясь в одной сети WiFi можно перейти на сайт сервера по ссылке:
```bash
http://<server_ip>:<server_port>
```
2. На главной странице можно зарегистрироваться или авторизоваться. 
<br>Зарегистрированные пользователи хранятся в `users.json` файле на сервере.
3. После того как пользователь зайдет в свой аккаунт ему откроется возможность загружать и отправлять свое изображение.
4. Отправленные изображения хранятся в `server/images` с названием `<filename>_<timestamp>_<uniqie_id>.jpg`

[//]: # (# Работа с камерой)

[//]: # (1. Запустите `camera.py`:)

[//]: # (```bash)

[//]: # (python -m webcamera_test.camera)

[//]: # (```)

[//]: # (Произойдет подключение к устройству захвата изображения, снимок с камеры будет сохранен )

[//]: # (по пути `webcamera_test/camera_images` в цветном и ч/б форматах.<br>)

[//]: # ()
[//]: # ([//]: # &#40;Передача изображения на сервер с устройства захвата изображения пользователя не оптимизирована и&#41;)
[//]: # ()
[//]: # ([//]: # &#40;не протестирована. Требуется доработка кода. &#41;)
# Безопасность
Пользователи создаются и хранятся на сервере в формате `имя_пользователя:hashed_pass`.
#### Плюсы:
- Пароли хранятся в hash-формате 
- Внутри маленькой сети имена пользователей и их пароли будет знать только администратор сервера
#### Минусы:
- Нет возможности регистрации для новых пользователей без участия администратора
- Внутри большой сети администратор не должен участвовать в авторизации новых пользователей
##### Должна будет предусмотрена возможность регистрации для новых пользователей
##### Нужно рассмотреть другие способы защиты сети (Например: VPN)
# Структура проекта
```plaintext
mqtt/
├── server/
│   ├── images/
│   │   └── received_image.jpg
│   ├── http_server.py
│   ├── upload_form.html
│   ├── gallery.html
│   └── server.py
├── client/
│   ├── test.jpg 
│   └── client.py
├── webcamera_test/
│   ├── camera_images/
│   │   └── camera_image.jpg
│   └── camera.py
├── requirements.txt
├── passwords.txt
├── config.py
├── mqtt_client.py
└── readme.md
```

