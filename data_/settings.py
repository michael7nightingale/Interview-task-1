"""
Файл с конфигурациями.
"""


# строго для src/tables.py
import os

TABLES = {
    "ALLOWED_EXTENSIONS": frozenset("csv", )

}

# строго для src/celebration_generator.py
CELEBRATION_GENERATOR = {
    "MESSAGE": """Напиши поздравление для друга __name__ в его день рождения, который родился 
    __birthday__. Сделай это душевно и лаконично, всё таки это день рождения. Не забудь упомянуть его дату рождения.""",
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