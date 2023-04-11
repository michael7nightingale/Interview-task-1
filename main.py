"""
Демонстрация функционала без Flask
"""

from src import tables, celebration_generator
from data_.settings import CELEBRATION_GENERATOR as CG


if __name__ == "__main__":
    # создаем менеджер таблиц
    table_manager = tables.PandasTableManager('d:/Progs/PycharmProjects/interview/app/corridor/data.csv')
    table_manager.open_data()
    print(table_manager.data)
    # генерация поздравлений
    celebrator = celebration_generator.Celebrator(token=CG['TOKEN'])
    celebrations = celebrator.generate_celebrations(
        data=table_manager.get_list_of_dicts_data()
    )
    # добавление поздравлений в таблицу
    table_manager.add_column(column_name='celebrations',
                             column_data=celebrations,
                             nullable=False)
    # сохраняем данные
    table_manager.save_data(filepath=None)




