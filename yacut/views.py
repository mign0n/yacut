from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_exists


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id and is_exists(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        short_id = custom_id if custom_id else get_unique_short_id()
        db.session.add(
            URLMap(
                original=form.original_link.data,
                short=short_id,
            )
        )
        db.session.commit()
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                'short_url_view',
                _external=True,
                short_id=short_id,
            ),
        )
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def short_url_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
