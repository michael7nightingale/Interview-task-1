class DeletingModeException(Exception):
    """Для работы в режиме удаления установите delete_mode = True"""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddLineException(Exception):
    """Количество аргументов не соответствует количеству столбцов."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddColumnException(Exception):
    """Количество аргументов не соответствует количеству строк."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class ColumnDoesNotExists(Exception):
    """Колонна с данным именем не существует."""


class InvalidDataFormat(Exception):
    """Неверный формат данных list[dict['name': str, 'birthday': str]]"""


class FileExtensionError(Exception):
    """Разрешение данного файла запрещено"""
