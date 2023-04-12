"""
Веб-система поздравлений. Запуск через терминал или вручную.
"""
import asyncio
import os
from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for, flash

from data_.settings import APP, SERVER, CELEBRATION_GENERATOR
from src import tables, exceptions, celebration_generator

# экземпляр приложения с названием по соглашению
app = Flask(__name__)
# импорт настроек
app.config = dict(
    tuple(app.config.items()) + tuple(APP.items())
)


@app.get("/")
def main_get():
    """Главная страница при GET-запросе"""
    return render_template("main.html")


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
    """Генерация поздравлений."""
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


# def save_and_delete(func):
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         os.remove(kwargs['path_or_file'])
#         return result
#     return wrapper


@app.post("/upload_file/")
def upload_file():
    """Загрузка и обработка файла."""
    try:
        file = request.files['file']
        print(file and verify_filename(file.filename))
        if file and verify_filename(file.filename):
            print(app.config['UPLOAD_FOLDER'])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # асинхронная генерация
            async_generate_celebrations(filepath)
            # или можно синхронно:
            # generate_celebrations(filepath)

            # после обработки отправляем файл пользователю
            return send_file(path_or_file=filepath, as_attachment=True)

        # если не прошли условия
        flash('Incorrect file extension or data')
    except Exception as error:
        # отображаем пользователю ошибку, если она нашлась
        flash(str(error))
    # редирект на главную страницу
    return redirect(url_for('main_get'))


def verify_filename(filename: str) -> bool:
    """Проверка расширения файла"""
    try:
        return '.' in filename and filename.rsplit('.', 1)[1] in APP["ALLOWED_EXTENSIONS"]
    except IndexError or TypeError:
        pass
    return False


# запуск приложения
if __name__ == '__main__':
    app.run(host=SERVER['HOST'],
            port=SERVER["PORT"],
            debug=True)
