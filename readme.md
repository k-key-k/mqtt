# MQTT Image Server
# Описание
Приём изображений через HTTP и MQTT в одной WI-FI сети, с сохранением их на сервере.
# Требования 
- Python 3.9
- Mosquitto
# Установка
1. Установите архив с Python 3.9, если он не установлен с [официального сайта](https://www.python.org/downloads/release/python-3913/)
2. Для того чтобы использовать нужную версию Python в проекте, создайте виртуальное окружение с версией Python 3.9:
   1. Откройте терминал (или командную строку) и перейдите в директорию вашего проекта.
   2. Создайте виртуальное окружение, указывая путь к Python 3.9, скачанному в предыдущем пункте:
   **Windows**
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
   4. Клонируйте репозиторий и перейдите в него:
   **Windows**
   ```bash
   git clone https://github.com/k-key-k/mqtt.git
   cd mqtt
   ```
   5. Установите все зависимости проекта, указанные в файле `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройка виртуального окружения в PyCharm:
   1. Перейдите в меню `File` → `Settings` → `Project: <project_name>` → `Python Interpreter`.
   2. Нажмите на иконку шестерёнки в правом верхнем углу и выберите `Add...`.
   3. В открывшемся окне выберите `New environment`.
   4. Нажмите на значок папки и укажите путь к интерпретатору Python в созданном виртуальном окружении:
   ```bash
   <path_to_project>\venv39\Scripts\python.exe
   ```
   5. Нажмите ОК для сохранения настроек.
4. На устройстве с сервером добавьте правило для подключения по порту в настройках брандмауэра Windows.
# Запуск
1. Установите ваш IP в upload_form.html:
> 72 fetch('http://0:0:0:0:8000/upload/', {<br>
  73                  method: 'POST',<br>
  74                  body: formData<br>
  75              })
2. В mosquitto.conf добавьте прослушивание на свободном порте и подключение анонимных пользователей:
```bash
listener free_port
allow_anonymous true
```
3. Запустите брокер Mosquitto с конфигурационным файлом:
```bash
"C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf" -v
```
4. Запустите сервер:
```bash
python .\server\server.py
```

# Структура проекта

```plaintext
project_name/
├── requirements.txt
├── readme.md
├── upload_form.html
├── server/
│   ├── images/
│   │   └── image.jpg
│   └── server.py
├── client/
│   └── client.py
└── webcamera_test/
    └── camera.py
```

# Использование
- С клиентского устройства перейдите по ссылке: http://**ip**:**port**/
- Загрузите изображение с клиентского устройства
- Изображение сохранится на сервере в папке проекта: .\images\
