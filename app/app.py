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
    table = tables.CsvTableManager(filepath, False, 0)
    table.open_data()
    celebrator = celebration_generator.Celebrator(token=CELEBRATION_GENERATOR['TOKEN'])
    new_data_column = celebrator.generate_celebrations(
        table.get_list_of_dicts_data()
    )
    table.add_column(column_name='celebrations',
                     column_data=new_data_column,
                     nullable=True)
    table.save_data(None)



@app.post("/upload_file/")
def upload_file():
    file = request.files['file']
    if file and verify_file(file.filename):
        print(123)
        print(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        generate_celebrations(filepath)

        # после обработки отправляем файл пользователю
        return send_file(path_or_file=filepath,
                         as_attachment=True)

    # если не прошли условия
    flash('Incorrect file extension or data')
    redirect(url_for('main_get'))


def verify_file(filename: str) -> bool:
    try:
        return '.' in filename and filename.rsplit('.', 1)[1] in APP["ALLOWED_EXTENSIONS"]
    except IndexError or TypeError:
        return False



# запуск приложения
if __name__ == '__main__':
    app.run(host=SERVER['HOST'],
            port=SERVER["PORT"],
            debug=True)
