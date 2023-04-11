from abc import ABC, abstractmethod
from typing import Sequence
import pandas as pd
import csv

from src import exceptions


class BaseTableManager(ABC):
    """Базовый интерфейс для работы с табличными данными."""
    def __init__(self, filepath: str, delete_mode: bool = False, default=""):
        self.filepath = filepath
        self._delete_mode = delete_mode
        self.default = default
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        if not self._data:
            # if type(new_data) == list[dict]:
                self._data = new_data

    @abstractmethod
    def open_data(self) -> None:
        """Открыть и установить данные по указанному пути"""
        pass

    @abstractmethod
    def get_column_data(self, column_name: str) -> tuple:
        pass

    @abstractmethod
    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        """Добавить колонку в таблицу."""
        pass

    @abstractmethod
    def add_line(self, args: Sequence = tuple(),
                 nullable: bool = False) -> None:
        """Добавить строку в таблицу"""
        pass

    @abstractmethod
    def delete_column(self, column_name: str) -> None:
        pass

    @abstractmethod
    def get_list_of_dicts_data(self) -> list[dict]:
        pass

    @abstractmethod
    def save_data(self, filepath=None) -> None:
        """Сохранение файла."""
        pass


class CsvTableManager(BaseTableManager):
    """Расширение для работы с табличными данными c помощью библиотеки csv."""
    _data: list[dict]
    columns: list

    def open_data(self):
        with open(self.filepath) as csv_file:
            self._data = list(csv.DictReader(csv_file))
        self.columns = list(self._data[0].keys())

    def add_line(self, line_data: Sequence = tuple(),
                 nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self.columns) - len(line_data) if (len(self.columns) - len(line_data) >= 0) else 0
            self._data.append(
                dict(
                    zip(self.columns,
                        (tuple(line_data) + tuple((self.default for i in range(nulls_to_add))))[:len(self.columns)]
                        )
                    )
                             )
        else:
            if len(line_data) != len(self.columns):
                raise exceptions.AddLineException()
            else:
                self._data.append(dict(zip(self.columns, line_data)))

    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        if nullable:
            nulls_to_add = len(self._data) - len(column_data) if (len(self._data) - len(column_data)) >= 0 else 0
            column_data = tuple(column_data) + tuple((self.default for _ in range(nulls_to_add)))
        else:
            if len(column_data) != len(self.columns):
                raise exceptions.AddColumnException()
        # добавляем новую колонку в данные
        self.columns.append(column_name)
        for line_number in range(len(self._data)):
            self._data[line_number][column_name] = column_data[line_number]

    def get_column_data(self, column_name: str) -> tuple:
        if column_name not in self.columns:
            raise exceptions.ColumnDoesNotExists
        return tuple((i[column_name] for i in self._data))

    def get_list_of_dicts_data(self) -> list[dict]:
        return self._data

    def delete_column(self, column_name: str) -> None:
        # если выключен режим удаления
        if not self._delete_mode:
            raise exceptions.DeletingModeException
        # если колонны с таки именем не существует
        if column_name not in self.columns:
            raise exceptions.ColumnDoesNotExists
        # если такая колонна есть
        for line in self._data:
            del line[column_name]

    def save_data(self, filepath=None) -> None:
        if filepath is None:
            filepath = self.filepath
        with open(filepath, 'w') as f:
            writer = csv.DictWriter(
                f, fieldnames=list(self._data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for d in self._data:
                writer.writerow(d)
        return filepath


class PandasTableManager(BaseTableManager):
    """Расширение для работы с табличными данными c помощью библиотеки pandas
    (`pd` - синоним)."""
    _data = pd.DataFrame
    columns = pd.Index

    def open_data(self) -> None:
        self._data: pd.DataFrame = pd.read_csv(self.filepath)
        self.columns: list = list(self._data.columns)

    def get_column_data(self, column_name: str) -> tuple:
        if column_name not in self.columns:
            raise exceptions.ColumnDoesNotExists
        return tuple(self._data[column_name])

    def add_line(self, args: Sequence = tuple(),
                 nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self.columns) - len(args) if (len(self.columns) - len(args) >= 0) else 0
            self._data.append.loc[len(self._data)] = \
                (list(args) + [self.default for _ in range(nulls_to_add)])[:len(self._data)]
        else:
            if len(args) != len(self.columns):
                raise exceptions.AddLineException()
            else:
                self._data.loc[len(self._data)] = args

    def add_column(self, column_name: str,
                   column_data: Sequence = tuple(),
                   nullable: bool = False) -> None:
        if nullable:
            nulls_to_add: int = len(self._data.values) - len(column_data) if (len(self._data.values) - len(column_data)) >= 0 else 0
            self._data[column_name] = (list(column_data) + ["" for _ in range(nulls_to_add)])[:len(self._data.values)]
        else:
            if len(column_data) != len(self.columns):
                raise exceptions.AddColumnException()
            else:
                self._data[column_name] = column_data
        self.columns.append(column_name)

    def delete_column(self, column_name: str) -> None:
        # если выключен режим удаления
        if not self._delete_mode:
            raise exceptions.DeletingModeException
        # если колонны с таки именем не существует
        if column_name not in self.columns:
            raise exceptions.ColumnDoesNotExists
        # если такая колонна есть
        del self._data[column_name]

    def get_list_of_dicts_data(self) -> list[dict]:
        return [
            dict(zip(
                self.columns, line
            )) for line in self._data.values
        ]

    def save_data(self, filepath=None) -> None:
        if filepath is None:
            filepath = self.filepath
        self._data.to_csv(filepath)


if __name__ == '__main__':
    table = PandasTableManager('test.csv', True, 0)
    table.open_data()
    print(table.add_column('mama', nullable=True))
    print(table.columns)
    print(table.get_list_of_dicts_data())

