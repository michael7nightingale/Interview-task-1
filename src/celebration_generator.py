"""
Функционал ChatGTP API для генерации поздравлений.
"""
import asyncio
import openai
from abc import ABC, abstractmethod

from data_.settings import CELEBRATION_GENERATOR
from src import exceptions


class BaseCelebrator(ABC):
    def __init__(self, token: str):
        self.__token = token
        openai.api_key = self.__token

    @staticmethod
    def replace_message_with_data(name: str, birthday: str) -> str:
        """Заменяет служебные пропуски в шаблоне запроса на данные"""
        return CELEBRATION_GENERATOR['MESSAGE'].replace('__name__', name).replace('__birthday__', birthday)

    @staticmethod
    @abstractmethod
    def chat(message: str) -> str:
        pass

    @abstractmethod
    def generate_celebrations(self, data: list[dict]) -> list[str]:
        pass


class Celebrator(BaseCelebrator):
    """Класс ПОЗДРАВЛЯТОР-3000 для Chat-GTP API."""

    @staticmethod
    def chat(message: str) -> str:
        """Функция общения с API Chat-GPT. Единственный вопрос - единственный ответ."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print(response.choices[0]['text'])  # для отладки
        return response.choices[0]['text']

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


class AsyncCelebrator(BaseCelebrator):
    """Асинхронный класс, то есть запросы к API происходят параллельно в рамках подзадач."""

    @staticmethod
    async def chat(message: str) -> str:
        """Функция общения с API Chat-GPT. Единственный вопрос - единственный ответ."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Сделай поздравление человеку с именем {message}. Добавь в него юмор",
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # из-за проблем с кодировкой пришлось обработать строку именно так
        return response.choices[0]['text'].replace('\n', '').replace('\c', '')[1:]

    async def generate_celebrations(self, data: list[dict]) -> list[str]:
        """Генерация списка поздравлений"""
        # проверка на валидность формата представления данных
        if all(CELEBRATION_GENERATOR["NAME_COLUMN"] in line and CELEBRATION_GENERATOR["BIRTHDAY_COLUMN"] in line for
               line in data):
            tasks = []
            for person in data:
                task = asyncio.create_task(self.chat(
                    self.replace_message_with_data(str(person['name']), str(person['birthday']))
                ))
                tasks.append(task)
                # print(task)     # для отладки
            res = await asyncio.gather(*tasks)
            return res
        else:
            raise exceptions.InvalidDataFormat



if __name__ == '__main__':
    c = Celebrator(CELEBRATION_GENERATOR['TOKEN'])
    print(c.chat('Напиши поздравление для друга Матвея в его день рождения, который родился 15.10.\
     Сделай это душевно и лаконично, всё таки это день рождения.'))

