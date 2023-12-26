from random import choices
from string import ascii_letters, digits

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


def is_exists(uri):
    return URLMap.query.filter_by(short=uri).first() is not None


def get_unique_short_id(size=app.config['DEFAULT_SHORT_URI_SIZE']):
    short_id = ''.join(choices(ascii_letters + digits, k=size))
    if is_exists(short_id):
        return get_unique_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id and is_exists(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        short_id = custom_id if custom_id else get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url_map)
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
    abort(404)
