from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from yacut import app

CREATE = 'Создать'
CUSTOM_SHORT_LINK = 'Ваш вариант короткой ссылки'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(1, app.config['ORIGINAL_LINK_MAX_SIZE']),
            URL(),
        ],
    )
    custom_id = URLField(
        CUSTOM_SHORT_LINK,
        validators=[Length(1, app.config['SHORT_ID_MAX_SIZE']), Optional()],
    )
    submit = SubmitField(CREATE)
