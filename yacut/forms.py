from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError, validators

from yacut import app
from yacut.api_views import SHORT_LINK_IS_EXISTS
from yacut.models import URLMap

CREATE = 'Создать'
CUSTOM_SHORT_LINK = 'Ваш вариант короткой ссылки'
INVALID_SHORT_LINK_NAME = 'Указано недопустимое имя для короткой ссылки'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'


def validate_unique(form, field):
    if URLMap.get(field.data) is not None:
        raise ValidationError(SHORT_LINK_IS_EXISTS)


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            validators.DataRequired(message=REQUIRED_FIELD),
            validators.Length(max=app.config['ORIGINAL_LINK_MAX_SIZE']),
            validators.URL(),
        ],
    )
    custom_id = URLField(
        CUSTOM_SHORT_LINK,
        validators=[
            validators.Length(max=app.config['SHORT_ID_MAX_SIZE']),
            validators.Optional(),
            validators.Regexp(
                app.config['SHORT_ID_PATTERN'],
                message=INVALID_SHORT_LINK_NAME,
            ),
            validate_unique,
        ],
    )
    submit = SubmitField(CREATE)
