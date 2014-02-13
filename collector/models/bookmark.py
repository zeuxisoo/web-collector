# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Bookmark(db.Model, SessionMixin):
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type      = db.Column(db.Enum('stream', 'the_of_girl'), nullable=False, default='stream')
    user_id   = db.Column(db.Integer, index=True)
    target_id = db.Column(db.Integer, index=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Bookmark: %s>' % self.id