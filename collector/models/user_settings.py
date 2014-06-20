# coding: utf-8

from datetime import datetime
from .base import db, SessionMixin

class UserSettings(db.Model, SessionMixin):
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id          = db.Column(db.Integer)
    public_profile   = db.Column(db.Integer)
    create_at        = db.Column(db.DateTime, default=datetime.utcnow)
    update_at        = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<UserSettings: %s>' % self.id
