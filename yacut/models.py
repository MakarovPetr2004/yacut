import random
import string
from datetime import datetime

from flask import url_for

from yacut import db
from . import constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(constants.MAX_ORIGINAL_LENGTH),
                         nullable=False)
    short = db.Column(db.String(constants.MAX_CUSTOM_ID_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short = kwargs.get('short') or self.generate_unique_short_url()

    @staticmethod
    def generate_unique_short_url() -> str:
        characters = string.ascii_letters + string.digits
        short = ''.join(
            random.choice(characters) for _ in range(constants.MAX_LENGTH))
        while URLMap.query.filter_by(short=short).first():
            short = ''.join(
                random.choice(characters) for _ in range(constants.MAX_LENGTH))
        return short

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('link_view', short=self.short, _external=True),
        )
