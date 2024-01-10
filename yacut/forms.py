from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut import app

CREATE = 'Создать'
CUSTOM_SHORT_LINK = 'Ваш вариант короткой ссылки'
INVALID_SHORT_LINK_NAME = 'Указано недопустимое имя для короткой ссылки'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=app.config['ORIGINAL_LINK_MAX_SIZE']),
            URL(),
        ],
    )
    custom_id = URLField(
        CUSTOM_SHORT_LINK,
        validators=[
            Length(max=app.config['SHORT_ID_MAX_SIZE']),
            Optional(),
            Regexp(
                app.config['SHORT_ID_PATTERN'],
                message=INVALID_SHORT_LINK_NAME,
            ),
        ],
    )
    submit = SubmitField(CREATE)
