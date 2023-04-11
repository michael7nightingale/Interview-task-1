"""
Функционал ChatGTP API для генерации поздравлений.
"""

import openai
from data_.settings import CELEBRATION_GENERATOR
from src import exceptions


class Celebrator:
    """Класс ПОЗДРАВЛЯТОР-3000 для Chat-GTP API."""
    def __init__(self, token: str):
        self.__token = token
        openai.api_key = self.__token

    def chat(self, message: str) -> str:
        """Функция общения с API Chat-GPT. Единственный вопрос - единственный ответ."""
        chat_ = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': "user", "content": message}
            ]
        )
        print(chat_.choices[0].message.content)
        return chat_.choices[0].message.content

    def generate_celebrations(self, data: list[dict]) -> list[str]:
        """Генерация списка поздравлений"""
        # проверка на валидность формата представления данных
        if all(CELEBRATION_GENERATOR["NAME_COLUMN"] in line and CELEBRATION_GENERATOR["BIRTHDAY_COLUMN"] in line for line in data):
            return [self.chat(
                self.replace_message_with_data(str(person['name']), str(person['birthday']))
            ) for person in data
                   ]
        else:
            raise exceptions.InvalidDataFormat

    @staticmethod
    def replace_message_with_data(name: str, birthday: str) -> str:
        """Заменяет служебные пропуски в шаблоне запроса на данные"""
        return CELEBRATION_GENERATOR['MESSAGE'].replace('__name__', name).replace('__birthday__', birthday)


if __name__ == '__main__':
    c = Celebrator(CELEBRATION_GENERATOR['TOKEN'])
    print(c.chat('Напиши поздравление для друга Матвея в его день рождения, который родился 15.10.\
     Сделай это душевно и лаконично, всё таки это день рождения.'))

