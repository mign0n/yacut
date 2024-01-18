from http import HTTPStatus

from flask import jsonify, request, url_for
from sqlalchemy.exc import SQLAlchemyError
from wtforms import ValidationError

from settings import SHORT_URL_VIEW
from yacut import app
from yacut.errors_handlers import InvalidAPIUsage
from yacut.models import URLMap

DB_ERROR = 'Сбой при выполнении операции с базой данных'
ID_NOT_FOUND = 'Указанный id не найден'
IS_A_REQUIRED_FIELD = '"url" является обязательным полем!'
NO_REQUEST_BODY = 'Отсутствует тело запроса'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    original_url = data.get('url')
    if not original_url:
        raise InvalidAPIUsage(IS_A_REQUIRED_FIELD)
    short_id = data.get('custom_id')

    try:
        url_map = URLMap.create(original_url, short_id)
    except SQLAlchemyError:
        raise InvalidAPIUsage(DB_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
    except ValidationError as error:
        message, *_ = error.args
        raise InvalidAPIUsage(message)
    return (
        jsonify(
            {
                'url': url_map.original,
                'short_link': url_for(
                    SHORT_URL_VIEW,
                    _external=True,
                    short_id=url_map.short,
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_link(short_id):
    try:
        return jsonify({'url': URLMap.get(short_id).original})
    except SQLAlchemyError:
        raise InvalidAPIUsage(DB_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
    except AttributeError:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
