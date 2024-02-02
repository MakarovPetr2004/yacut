import random
import string
from datetime import datetime

from flask import url_for

from yacut import db
from .constants import MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short = kwargs.get('short') or self.generate_unique_short_url()

    def generate_unique_short_url(self) -> str:
        characters = string.ascii_letters + string.digits
        short = ''.join(random.choice(characters) for _ in range(MAX_LENGTH))
        while URLMap.query.filter_by(short=short).first():
            short = ''.join(random.choice(characters) for _ in range(MAX_LENGTH))
        return short

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('link_view', short=self.short, _external=True),
        )

    def from_dict(self, data):
        to_model_field = {
            'url': 'original',
            'custom_id': 'short'
        }

        for field, model_field in to_model_field.items():
            if field in data:
                setattr(self, model_field, data[field])

