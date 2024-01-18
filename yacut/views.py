from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for
from wtforms import ValidationError

from settings import SHORT_URL_VIEW
from yacut import app
from yacut.errors_handlers import GenerationError, InvalidAPIUsage
from yacut.forms import URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                SHORT_URL_VIEW,
                _external=True,
                short_id=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data,
                ).short,
            ),
        )
    except ValidationError as error:
        message, *_ = error.args
        flash(message)
    except GenerationError as error:
        message, *_ = error.args
        raise InvalidAPIUsage(message, HTTPStatus.INTERNAL_SERVER_ERROR)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def short_url_view(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
