import re

from flask import jsonify, request

from . import app, db
from .constants import CUSTOM_ID_REGEX
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<path:short>/', methods=['GET'])
def get_link(short):
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    custom_id = data.get('custom_id')
    if custom_id:
        if (len(custom_id) > 16
                or re.match(CUSTOM_ID_REGEX, custom_id) is None):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                400
            )

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                400
            )
    urlmap = URLMap(
        original=data['url'],
        short=custom_id
    )

    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
