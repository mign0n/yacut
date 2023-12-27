import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.errors_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_exists


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original_url = data.get('url')
    custom_id = data.get('custom_id')
    if not original_url:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if custom_id:
        if len(custom_id) > app.config['SHORT_ID_MAX_SIZE']:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if re.fullmatch(r'[0-9a-zA-Z]+', custom_id) is None:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if is_exists(custom_id):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_id = get_unique_short_id()

    db.session.add(URLMap(original=original_url, short=custom_id))
    db.session.commit()
    return (
        jsonify(
            {
                'url': original_url,
                'short_link': url_for(
                    'short_url_view', _external=True, short_id=custom_id
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original})
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
