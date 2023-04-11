class DeletingModeException(BaseException):
    """Для работы в режиме удаления установите delete_mode = True"""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddLineException(BaseException):
    """Количество аргументов не соответствует количеству столбцов."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class AddColumnException(BaseException):
    """Количество аргументов не соответствует количеству строк."""

    def __call__(self, *args, **kwargs):
        print(self.__doc__)


class ColumnDoesNotExists(BaseException):
    """Колонна с данным именем не существует."""


class InvalidDataFormat(BaseException):
    """Неверный формат данных list[dict['name': str, 'birthday': str]]"""


