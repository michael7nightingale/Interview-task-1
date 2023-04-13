"""
Демонстрация функционала без Flask
"""
import asyncio


from src import tables, celebration_generator
from data_.settings import CELEBRATION_GENERATOR


def generate_celebrations(filepath: str):
    """Генерация поздравлений."""
    # инициализация таблицы
    table = tables.CsvTableManager(filepath, False, 0)
    table.open_data()
    # генерация поздравлений
    celebrator = celebration_generator.Celebrator(token=CELEBRATION_GENERATOR['TOKEN'])
    new_data_column = celebrator.generate_celebrations(
        table.get_list_of_dicts_data()
    )
    # добавление и сохранение данных
    table.add_column(column_name='celebrations',
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


def async_generate_celebrations(filepath: str):
    """Генерация поздравлений, но асинхронно!!!"""
    # инициализация таблицы
    table = tables.CsvTableManager(filepath, False, 0)
    table.open_data()
    # генерация поздравлений
    celebrator = celebration_generator.AsyncCelebrator(token=CELEBRATION_GENERATOR['TOKEN'])
    new_data_column = asyncio.run(celebrator.generate_celebrations(
        table.get_list_of_dicts_data()
    ))
    # добавление и сохранение данных
    table.add_column(column_name='celebrations',
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


if __name__ == "__main__":
    filepath = 'd:/Progs/PycharmProjects/interview/app/corridor/data.csv'
    # асинхронная генерация
    async_generate_celebrations(filepath)
    # или можно синхронно:
    # generate_celebrations(filepath)

