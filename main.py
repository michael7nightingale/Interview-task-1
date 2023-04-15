"""
Демонстрация функционала без Flask
"""
import asyncio


from src import tables, celebration_generator
from data_.settings import CELEBRATION_GENERATOR


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
    new_data_column = asyncio.run(
        celebrator.generate_celebrations(data=table.get_list_of_dicts_data(),
                                         name_column=name_column,
                                         birthday_column=birthday_column)
        )

    # добавление и сохранение данных
    table.add_column(column_name=celebration_column,
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)


if __name__ == "__main__":
    filepath = 'd:/KING/data (2).csv'
    # асинхронная генерация
    generate_celebrations(filepath=filepath,
                          birthday_column=CELEBRATION_GENERATOR['BIRTHDAY_COLUMN'],
                          name_column=CELEBRATION_GENERATOR['NAME_COLUMN'],
                          celebration_column='celebrations',
                          api_key=CELEBRATION_GENERATOR["TOKEN"])
    # или можно синхронно:
    # generate_celebrations(filepath)

