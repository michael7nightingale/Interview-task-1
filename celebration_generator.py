import openai
from config import CELEBRATION_GENERATOR
import tables
import exceptions


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
        return chat_.choices[0].message.content

    def generate_celebrations(self, data: list[dict]) -> list:
        """Генерация списка поздравлений"""
        # проверка на валидность формата представления данных
        if all("name" in line and "birthday" in line for line in data):
            return [self.chat(
                self.replace_message_with_data(person['name'], person['birthday'])
            ) for person in data
                   ]
        else:
            raise exceptions.InvalidDataFormat

    @staticmethod
    def replace_message_with_data(name: str, birthday: str) -> str:
        """Заменяет служебные пропуски в шаблоне запроса на данные"""
        return CELEBRATION_GENERATOR['MESSAGE'].replace('__name__', name).replace('__birthday__', birthday)


