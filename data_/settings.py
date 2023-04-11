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
    __birthday__. Сделай это душевно и лаконично, всё таки это день рождения.""",
    "TOKEN": "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",
    "NAME_COLUMN": "name",
    "BIRTHDAY_COLUMN": 'birthday',

}

# строго для app/app.py
APP = {
    "UPLOAD_FOLDER": os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('data_', 'app', -1), 'corridor/'),
    "ALLOWED_EXTENSIONS": frozenset(("csv", )),

}

SERVER = {
    "HOST": "localhost",
    "PORT": 5000,
}