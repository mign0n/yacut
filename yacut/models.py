from datetime import datetime
from random import choices

from yacut import app, db
from yacut.errors_handlers import GenerationError

SHORT_LINK_GENERATION_ERROR = 'Ошибка генерации короткой ссылки.'


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
        url_map = URLMap(original=original_url, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()
