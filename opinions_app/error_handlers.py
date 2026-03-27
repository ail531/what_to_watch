from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    # Если статус-код для ответа API не указан, вернётся код 400.
    status_code = 400

    # Конструктор класса InvalidAPIUsage принимает на вход
    # текст сообщения и статус-код ошибки (необязательно).
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        # Если статус-код передан в конструктор,
        # этот код вернётся в ответе.
        if status_code is not None:
            self.status_code = status_code

    # Метод для сериализации переданного сообщения об ошибке.
    def to_dict(self):
        return dict(message=self.message)


# Обработчик кастомного исключения для API.
# Flask запоминает: "Для исключений типа InvalidAPIUsage
# вызывать функцию invalid_api_usage"
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    # Возвращает в ответе текст ошибки и статус-код.
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    # При ошибке 404 в качестве ответа вернётся страница, созданная
    # на основе шаблона 404.html и код HTTP-ответа 404.
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # Ошибка 500 возникает в нештатных ситуациях на сервере.
    # Например, провалилась валидация данных.
    # В таких случаях можно откатить изменения, незафиксированные в БД,
    # чтобы в базу не записалось ничего лишнего.
    db.session.rollback()
    # Пользователю вернётся страница, сгенерированная на основе шаблона 500.html.
    # Этого шаблона пока нет, но сейчас вы его тоже создадите.
    # Пользователь получит и код HTTP-ответа 500.
    return render_template('500.html'), 500
