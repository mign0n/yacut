# YaCut

## Описание

Сервис для укорачивания URL-адресов.

## Технологии

- [Python v3.9](https://docs.python.org/3.9/)
- [Flask v2.0](https://flask.palletsprojects.com/en/2.0.x/)
- [SQLAlchemy v1.4](https://docs.sqlalchemy.org/en/14/)

## Запуск проекта на Linux

- Склонируйте репозиторий и перейдите в директорию проекта

```shell
git clone https://github.com/mign0n/yacut.git && cd yacut
```

- Установите и активируйте виртуальное окружение

```shell
python -m venv venv && source venv/bin/activate
```

- Установите зависимости из файла requirements.txt

```shell
pip install -r requirements.txt
```

- Создайте `.env` файл (при необходимости отредактируйте его)

```shell
cp .env.example .env
```

- Создайте базу данных

```shell
echo "from yacut import db; db.create_all()" | flask shell >/dev/null 2>&1
```

- Запустите веб-сервер и перейдите по адресу http://127.0.0.1:5000/

```shell
flask run
```

## API

API имеет два эндпоинта:

1. POST /api/id/ - для создания короткой ссылки

    ```shell
    curl --header "content-type:application/json" \
    --data '{"url": "http://example.com/"}' \
    --request POST http://127.0.0.1:5000/api/id/
    ```
    ```text
    {
      "short_link": "http://127.0.0.1:5000/o8yjhi",
      "url": "http://example.com/"
    }
    ```

2. GET /api/id/{short_id}/ - для получения оригинальной ссылки по короткой

    ```shell
    curl --header "content-type:application/json" \
    --request GET http://127.0.0.1:5000/api/id/o8yjhi/
    ```
    ```text
    {
      "url": "http://example.com/"
    }
    ```

## Авторы

- [Олег Сапожников](https://github.com/mign0n)
- [yandex-praktikum](https://github.com/yandex-praktikum)
