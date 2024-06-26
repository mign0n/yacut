import re
from datetime import datetime
from random import choices

from wtforms import ValidationError

from settings import ORIGINAL_LINK_PATTERN, SHORT_CHARACTERS, SHORT_PATTERN
from yacut import app, db
from yacut.errors_handlers import GenerationError

INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
INVALID_URL = 'Недействительный URL.'
SHORT_GENERATION_ERROR = 'Ошибка генерации короткой ссылки.'
SHORT_IS_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
URL_TOO_LONG = 'Длина URL не должна превышать {} символов.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(app.config['ORIGINAL_LINK_MAX_SIZE']))
    short = db.Column(db.String(app.config['SHORT_MAX_SIZE']), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id(
        size=app.config['DEFAULT_SHORT_SIZE'],
        max_iteration=app.config['MAX_ITERATION'],
        characters=SHORT_CHARACTERS,
    ):
        for _ in range(max_iteration):
            short = ''.join(choices(characters, k=size))
            if URLMap.get(short) is None:
                return short
        raise GenerationError(SHORT_GENERATION_ERROR)

    @staticmethod
    def create(original_url, short, need_validate=False):
        if need_validate:
            if len(original_url) > app.config['ORIGINAL_LINK_MAX_SIZE']:
                raise ValidationError(
                    URL_TOO_LONG.format(app.config['ORIGINAL_LINK_MAX_SIZE'])
                )
            if re.fullmatch(ORIGINAL_LINK_PATTERN, original_url) is None:
                raise ValidationError(INVALID_URL)
            if short:
                if (
                    len(short) > app.config['SHORT_MAX_SIZE']
                    or re.fullmatch(SHORT_PATTERN, short) is None
                ):
                    raise ValidationError(INVALID_SHORT_NAME)
                if URLMap.get(short) is not None:
                    raise ValidationError(SHORT_IS_EXISTS)
        if not short:
            short = URLMap.get_unique_short_id()
        url_map = URLMap(original=original_url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()
