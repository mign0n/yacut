from random import choices
from string import ascii_letters, digits

from yacut import app
from yacut.models import URLMap


def is_exists(uri):
    return URLMap.query.filter_by(short=uri).first() is not None


def get_unique_short_id(size=app.config['DEFAULT_SHORT_ID_SIZE']):
    short_id = ''.join(choices(ascii_letters + digits, k=size))
    if is_exists(short_id):
        return get_unique_short_id()
    return short_id
