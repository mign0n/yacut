import re
from datetime import datetime
from http import HTTPStatus
from random import choices
from string import ascii_letters, digits

from yacut import app, db
from yacut.errors_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(app.config['ORIGINAL_LINK_MAX_SIZE']))
    short = db.Column(db.String(app.config['SHORT_ID_MAX_SIZE']), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def is_exists(self, **kwargs):
        return self.query.filter_by(**kwargs).first() is not None

    def get_unique_short_id(self, size=app.config['DEFAULT_SHORT_ID_SIZE']):
        short_id = ''.join(choices(ascii_letters + digits, k=size))
        if self.is_exists(short=short_id):
            return self.get_unique_short_id()
        return short_id

    def validate(self, data):
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
            if self.is_exists(short=custom_id):
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
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
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
