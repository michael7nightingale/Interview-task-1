"""
Файл с конфигурациями.
"""

import os


# строго для src/tables.py
TABLES = {
    "ALLOWED_EXTENSIONS": frozenset(("csv", ))

}

# строго для src/celebration_generator.py
CELEBRATION_GENERATOR = {
    "MESSAGE": """Напиши поздравление для человека __name__ в день рождения, который родился 
    __birthday__. Сделай это душевно, всё таки это день рождения. Не забудь упомянуть дату рождения. Добавь юмора.""",
    "TOKEN": "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", # ВВЕДИТЕ РАБОЧИЙ API-КЛЮЧ!!! МОЙ БЛОКИРУЕТСЯ СПУСТЯ 30 МИНУТ ИЗ-ЗА ГЕОЛОКАЦИИ
    "NAME_COLUMN": "name",
    "BIRTHDAY_COLUMN": 'birthday',

}

# строго для app/app.py
APP = {
    "UPLOAD_FOLDER": os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('data_', 'app', -1), 'corridor/'),
    "ALLOWED_EXTENSIONS": frozenset(("csv", )),
    "SECRET_KEY": "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",

}

SERVER = {
    "HOST": "localhost",
    "PORT": 5000,
}