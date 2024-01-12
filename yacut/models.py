import re
from datetime import datetime
from http import HTTPStatus
from random import choices

from yacut import app, db
from yacut.errors_handlers import InvalidAPIUsage, GenerationError

ID_NOT_FOUND = 'Указанный id не найден'
INVALID_SHORT_LINK_NAME = 'Указано недопустимое имя для короткой ссылки'
IS_A_REQUIRED_FIELD = '"url" является обязательным полем!'
SHORT_LINK_GENERATION_ERROR = 'Ошибка генерации короткой ссылки.'
SHORT_LINK_IS_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(app.config['ORIGINAL_LINK_MAX_SIZE']))
    short = db.Column(db.String(app.config['SHORT_ID_MAX_SIZE']), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def is_exists(**kwargs):
        return URLMap.query.filter_by(**kwargs).first() is not None

    @staticmethod
    def get_unique_short_id(
        size=app.config['DEFAULT_SHORT_ID_SIZE'],
        max_iteration=app.config['MAX_ITERATION'],
        characters=app.config['SHORT_ID_CHARACTERS'],
    ):
        for _ in range(max_iteration):
            short_id = ''.join(choices(characters, k=size))
            if not URLMap.is_exists(short=short_id):
                return short_id
        raise GenerationError(SHORT_LINK_GENERATION_ERROR)

    @staticmethod
    def create(original_url, short_id=None):
        if not original_url:
            raise InvalidAPIUsage(IS_A_REQUIRED_FIELD)
        if short_id:
            if (
                len(short_id) > app.config['SHORT_ID_MAX_SIZE']
                or re.fullmatch(app.config['SHORT_ID_PATTERN'], short_id)
                is None
            ):
                raise InvalidAPIUsage(INVALID_SHORT_LINK_NAME)
            if URLMap.is_exists():
                raise InvalidAPIUsage(SHORT_LINK_IS_EXISTS)
        else:
            short_id = URLMap.get_unique_short_id()
        url_map = URLMap(
            original=original_url,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get(self, short_id):
        url_map = self.query.filter_by(short=short_id).first()
        if url_map is not None:
            return url_map
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
