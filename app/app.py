"""
Веб-система поздравлений. Запуск через терминал или вручную.
"""
import asyncio
import os
from time import time
from flask import Flask, render_template, request, redirect, send_file, url_for, flash

from data_.settings import APP, SERVER, CELEBRATION_GENERATOR, logger
from src import tables, exceptions, celebration_generator

# =========================КОНФИГУРАЦИЯ====================== #

# экземпляр приложения с названием по соглашению
app = Flask(__name__)
# импорт настроек
app.config = dict(
    tuple(app.config.items()) + tuple(APP.items())
)


# =======================ЛОГИКА=ПРИЛОЖЕНИЯ================== #

@app.get("/")
def main_get():
    """Главная страница при GET-запросе"""
    logger.info(f"__APP__...GET-запрос по адресу /")
    return render_template("main.html")


def generate_celebrations(filepath: str,
                          name_column: str,
                          birthday_column: str,
                          celebration_column: str,
                          api_key: str):
    """Генерация поздравлений."""
    # инициализация таблицы
    table = tables.CsvTableManager(filepath, False, 0)
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


# def save_and_delete(func):
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         os.remove(kwargs['path_or_file'])
#         return result
#     return wrapper


@app.post("/upload_file/")
def upload_file():
    """Загрузка и обработка файла."""
    logger.info(f"__APP__...POST-запрос по адресу /upload_file/")
    start_time = time()
    try:
        # данные из формы
        file = request.files['file']
        # дынные для неопытных
        name_column = request.form['name_column']
        birthday_column = request.form['birthday_column']
        celebration_column = request.form['celebration_column']
        api_key = request.form['api_key']
        # обработка данных из формы
        if file and verify_filename(file.filename):
            logger.info(f"__APP__ Путь до папки в коридоре: {app.config['UPLOAD_FOLDER']}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # асинхронная генерация
            # async_generate_celebrations(filepath=filepath,
            #                             name_column=name_column,
            #                             birthday_column=birthday_column,
            #                             celebration_column=celebration_column,
            #                             api_key=api_key)
            # или можно синхронно:
            generate_celebrations(filepath=filepath,
                                  name_column=name_column,
                                  birthday_column=birthday_column,
                                  celebration_column=celebration_column,
                                  api_key=api_key)
            # после обработки отправляем файл пользователю
            return send_file(path_or_file=filepath, as_attachment=True)
        # если не прошли условия
        logger.error(f"__APP__ Неразрешенное расширение файла")
        flash('Incorrect file extension or data', 'error')
    except Exception as error:
        # отображаем пользователю ошибку, если она нашлась
        logger.error("__APP__" + str(error))
        flash(str(error), 'error')
    finally:
        flash(str(time() - start_time), 'time')
    # редирект на главную страницу
    return redirect(url_for('main_get'))


def verify_filename(filename: str) -> bool:
    """Проверка расширения файла"""
    try:
        return '.' in filename and filename.rsplit('.', 1)[1] in APP["ALLOWED_EXTENSIONS"]
    except IndexError or TypeError:
        pass
    logger.warning(f"__APP__ Файл не прошел проверку на валидность расширения: {filename}")
    return False


# запуск приложения
if __name__ == '__main__':
    app.run(host=SERVER['HOST'],
            port=SERVER["PORT"],
            debug=True)
