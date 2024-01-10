import re
from datetime import datetime
from http import HTTPStatus
from random import choices

from yacut import app, db
from yacut.errors_handlers import InvalidAPIUsage

ID_NOT_FOUND = 'Указанный id не найден'
INVALID_SHORT_LINK_NAME = 'Указано недопустимое имя для короткой ссылки'
IS_A_REQUIRED_FIELD = '"url" является обязательным полем!'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
SHORT_LINK_IS_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(app.config['ORIGINAL_LINK_MAX_SIZE']))
    short = db.Column(db.String(app.config['SHORT_ID_MAX_SIZE']), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def is_exists(self, **kwargs):
        return self.query.filter_by(**kwargs).first() is not None

    def get_unique_short_id(
        self,
        size=app.config['DEFAULT_SHORT_ID_SIZE'],
        max_iteration=app.config['MAX_ITERATION'],
        characters=app.config['SHORT_ID_CHARACTERS'],
    ):
        iteration = 0
        short_id = ''.join(choices(characters, k=size))
        while self.is_exists(short=short_id) or iteration > max_iteration:
            short_id = ''.join(choices(characters, k=size))
            iteration += 1
        return short_id

    def validate(self, data):
        if data is None:
            raise InvalidAPIUsage(NO_REQUEST_BODY)
        original_url = data.get('url')
        custom_id = data.get('custom_id')
        if not original_url:
            raise InvalidAPIUsage(IS_A_REQUIRED_FIELD)
        if custom_id:
            if (
                len(custom_id) > app.config['SHORT_ID_MAX_SIZE']
                or re.fullmatch(app.config['SHORT_ID_PATTERN'], custom_id)
                is None
            ):
                raise InvalidAPIUsage(INVALID_SHORT_LINK_NAME)
            if self.is_exists(short=custom_id):
                raise InvalidAPIUsage(SHORT_LINK_IS_EXISTS)
        else:
            data['custom_id'] = self.get_unique_short_id()

        return data

    def create(self, data):
        validated_data = self.validate(data)
        url_map = URLMap(
            original=validated_data['url'],
            short=validated_data['custom_id'],
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get(self, short_id):
        url_map = self.query.filter_by(short=short_id).first()
        if url_map is not None:
            return url_map
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
