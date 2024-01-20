from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError, validators

from settings import SHORT_PATTERN
from yacut import app
from yacut.models import SHORT_IS_EXISTS, URLMap

CREATE = 'Создать'
CUSTOM_SHORT = 'Ваш вариант короткой ссылки'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'


def validate_unique(form, field):
    if URLMap.get(field.data) is not None:
        raise ValidationError(SHORT_IS_EXISTS)


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
        CUSTOM_SHORT,
        validators=[
            validators.Length(max=app.config['SHORT_MAX_SIZE']),
            validators.Optional(),
            validators.Regexp(
                SHORT_PATTERN,
                message=INVALID_SHORT,
            ),
            validate_unique,
        ],
    )
    submit = SubmitField(CREATE)
