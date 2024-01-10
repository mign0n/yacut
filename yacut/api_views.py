from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app
from yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    url_map = URLMap().create(request.get_json())
    return (
        jsonify(
            {
                'url': url_map.original,
                'short_link': url_for(
                    app.config['SHORT_URL_VIEW'],
                    _external=True,
                    short_id=url_map.short,
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_link(short_id):
    return jsonify({'url': URLMap().get(short_id).original})
