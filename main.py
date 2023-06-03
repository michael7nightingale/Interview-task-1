"""
Демонстрация функционала без Flask
"""
import asyncio

from src import tables, celebration_generator
from data_.settings import CELEBRATION_GENERATOR
import time


def thread_generate_celebrations(
        filepath: str,
        name_column: str,
        birthday_column: str,
        celebration_column: str,
        api_key: str):
    table = tables.PandasTableManager(filepath, False, 0)
    table.open_data()
    # генерация поздравлений
    celebrator = celebration_generator.ThreadCelebrator(token=api_key)
    new_data_column = celebrator.generate_celebrations(data=table.get_list_of_dicts_data(),
                                                       name_column=name_column,
                                                       birthday_column=birthday_column)
    # добавление и сохранение данных
    table.add_column(column_name=celebration_column,
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


def generate_celebrations(filepath: str,
                          name_column: str,
                          birthday_column: str,
                          celebration_column: str,
                          api_key: str):
    """Генерация поздравлений."""
    # инициализация таблицы
    table = tables.PandasTableManager(filepath, False, 0)
    table.open_data()
    # генерация поздравлений
    celebrator = celebration_generator.Celebrator(token=api_key)
    new_data_column = celebrator.generate_celebrations(data=table.get_list_of_dicts_data(),
                                                       name_column=name_column,
                                                       birthday_column=birthday_column)
    # добавление и сохранение данных
    table.add_column(column_name=celebration_column,
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


def async_generate_celebrations(filepath: str,
                                name_column: str,
                                birthday_column: str,
                                celebration_column: str,
                                api_key: str):
    """Генерация поздравлений."""
    # инициализация таблицы
    table = tables.CsvTableManager(filepath, False, 0)
    table.open_data()
    # генерация поздравлений
    celebrator = celebration_generator.AsyncCelebrator(token=api_key)
    new_data_column = celebrator.generate_celebrations(
        data=table.get_list_of_dicts_data(),
        name_column=name_column,
        birthday_column=birthday_column
    )

    # добавление и сохранение данных
    table.add_column(column_name=celebration_column,
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


if __name__ == "__main__":
    t = tables.CsvTableManager(filepath='d:/KING/data.csv')
    t.init_data(["name", "birthday"])
    data = [["Михаил", "14.10.2006"], ["Анюта", "14.10.2006"], ["Эмуль", "04.10.2006"], ["Абдул", "14.10.2006"], ]
    for inf in data:
        t.add_line(line_data=inf, nullable=False)
    t.save_data()
    filepath = 'd:/KING/data.csv'
    # асинхронная генерация
    time_ = time.perf_counter()
    async_generate_celebrations(
        filepath=filepath,
        birthday_column=CELEBRATION_GENERATOR['BIRTHDAY_COLUMN'],
        name_column=CELEBRATION_GENERATOR['NAME_COLUMN'],
        celebration_column='celebrations',
        api_key=CELEBRATION_GENERATOR["TOKEN"]
    )

    print("Time:", time.perf_counter() - time_)

