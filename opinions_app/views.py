# Импортировать функцию для случайного выбора объекта.
from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
# from .dropbox import upload_files_to_dropbox
from .dropbox import async_upload_files_to_dropbox
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route('/')
def index_view():
    # print(app.config)  # Посмотреть настройки проекта.
    opinion = random_opinion()
    # Если мнений нет...
    if opinion is None:
        abort(500)
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
async def add_opinion_view():
    # Создать новый экземпляр формы.
    form = OpinionForm()
    # Если ошибок не возникло...
    if form.validate_on_submit():
        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь...
        if Opinion.query.filter_by(text=text).first() is not None:
            # ...вызвать функцию flash и передать соответствующее сообщение.
            flash('Такое мнение уже было оставлено ранее!')
            # Вернуть пользователя на страницу «Добавить новое мнение».
            return render_template('add_opinion.html', form=form)

        # # Добавьте вызов функции загрузки файлов
        # # и передайте туда сами файлы.
        # urls = upload_files_to_dropbox(form.images.data)
        # Замените вызов синхронной функции на вызов асинхронной.

        # Обязательно добавьте ключевое слово await,
        # так как функция async_upload_files_to_dropbox() асинхронная.
        urls = await async_upload_files_to_dropbox(form.images.data)
        # ...то нужно создать новый экземпляр класса Opinion...
        opinion = Opinion(
            # ...и передать в него данные, полученные из формы.
            title=form.title.data,
            text=text,
            source=form.source.data,
            images=urls
        )
        # Затем добавить его в сессию работы с базой данных...
        db.session.add(opinion)
        # ...и зафиксировать изменения.
        db.session.commit()
        # Затем переадресовать пользователя на страницу добавленного мнения.
        return redirect(url_for('opinion_view', id=opinion.id))
    # Если валидация не пройдена - просто отрисовать страницу с формой.
    return render_template('add_opinion.html', form=form)


# Тут указывается конвертер пути для id.
@app.route('/opinions/<int:id>')
# Параметром указывается имя переменной.
def opinion_view(id):
    # Теперь можно запросить нужный объект по id...
    opinion = Opinion.query.get_or_404(id)
    # ...и передать его в шаблон (шаблон - тот же, что и для главной страницы).
    return render_template('opinion.html', opinion=opinion)
