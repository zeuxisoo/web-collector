# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Comment(db.Model, SessionMixin):
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category  = db.Column(db.Enum('stream', 'today'), nullable=False, default='stream')
    user_id   = db.Column(db.Integer, nullable=False)
    result_id = db.Column(db.Integer, nullable=False)
    content   = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<Comment: %s>' % self.id
