import re
from datetime import datetime
from random import choices

from wtforms import ValidationError

from yacut import app, db
from yacut.errors_handlers import GenerationError

INVALID_SHORT_LINK_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_LINK_GENERATION_ERROR = 'Ошибка генерации короткой ссылки.'
SHORT_LINK_IS_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(app.config['ORIGINAL_LINK_MAX_SIZE']))
    short = db.Column(db.String(app.config['SHORT_ID_MAX_SIZE']), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id(
        size=app.config['DEFAULT_SHORT_ID_SIZE'],
        max_iteration=app.config['MAX_ITERATION'],
        characters=app.config['SHORT_ID_CHARACTERS'],
    ):
        for _ in range(max_iteration):
            short_id = ''.join(choices(characters, k=size))
            if URLMap.get(short_id) is None:
                return short_id
        raise GenerationError(SHORT_LINK_GENERATION_ERROR)

    @staticmethod
    def create(original_url, short_id):
        if short_id:
            if (
                len(short_id) > app.config['SHORT_ID_MAX_SIZE']
                or re.fullmatch(app.config['SHORT_ID_PATTERN'], short_id)
                is None
            ):
                raise ValidationError(INVALID_SHORT_LINK_NAME)
            if URLMap.get(short_id) is not None:
                raise ValidationError(SHORT_LINK_IS_EXISTS)
        else:
            short_id = URLMap.get_unique_short_id()
        url_map = URLMap(original=original_url, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()
