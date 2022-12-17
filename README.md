# Kinopoisk (service with movies)
### - use for tests:
 ```shell 
python -m pytest tests
```
### - use for run project:
 ```shell 
flask run
```
### - дополнительно:
- swagger:
 ```shell 
http://127.0.0.1:5000/docs
```
- ./skypro_py_stand-main/README.md for start frontend

---

### Используемые технологии:
Flask , pytest, SQLAlchemy, Marshmallow, REST, CRUD, DAO, JWT, SQLite


### Задача: 
Написать backend для сервиса по поиску кинофильмов

## Запуск проекта
- Установка зависимостей
```shell
pip install -r requirements.txt

pip install -r requirements.dev.txt
```

- Создание моделей (очистит БД и создаст все модели, указанные в импорте)
```shell
python create_tables.py
```

- Загрузка данных в базу
```shell
python load_fixture.py
```
Скрпит читает файл fixtures.json и загружает данные в базу. Если данные уже загружены - выводит соответсвующее сообщение. 

## Запуск проекта

```shell
flask run
```

## Запуск тестов
```shell
pytest .
```

