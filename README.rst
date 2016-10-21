Flask SQLAlchemy Logger
=======================

Нехитрая приблуда, которая облагораживает логгирование SQL-запросов
SQLAlchemy в Flask-приложении. Основана на коде @neoden.

Установка и настройка
---------------------

.. code:: bash

    $ pip install git+https://github.com/uisky/flask-sa-logger

.. code:: python

    import flask
    import sqlalchemy
    import flask_sa_logger

    app = flask.Flask(__name__)
    app.config.from_mapping({
        'FLASK_SA_LOGGER': 'log'
    })

    flask_sa_logger.init_logging(app)

    engine = sa.create_engine('sqlite:///:memory:', echo=False)

У логгера два режима работы, определяемых значением
``config['FLASK_SA_LOGGER']``:

1. ``log`` или ``True``. Форматирует SQL-запросы при помощи модуля
   ``sqlparse``, раскрашивает ключевые слова и имена таблиц. Может
   работать и без Flask.
2. ``analyze`` или ``analyse``. Работает только с Flask. За всё время
   обработки HTTP-запроса, запоминает SQL-запросы, а потом выводит в
   консоль таблицу — запрос (без значений параметров) и количество его
   вызовов. Помогает отследить множественные lazy relationship loading.