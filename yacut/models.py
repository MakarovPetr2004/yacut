import string
import random
from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short_id(self, length=6):
        characters = string.ascii_letters + string.digits
        self.short = ''.join(random.choice(characters) for _ in range(length))
