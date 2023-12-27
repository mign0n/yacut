from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from yacut import app


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, app.config['ORIGINAL_LINK_MAX_SIZE']),
            URL(),
        ],
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, app.config['SHORT_ID_MAX_SIZE']), Optional()],
    )
    submit = SubmitField('Создать')
