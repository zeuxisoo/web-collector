# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class DropboxLog(db.Model, SessionMixin):
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category  = db.Column(db.Enum('stream', 'today'), nullable=False, default='stream')
    user_id   = db.Column(db.Integer, index=True)
    target_id = db.Column(db.Integer, index=True)
    status    = db.Column(db.Enum('success', 'failed'), nullable=False, default='success')
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<DropboxLog: %s>' % self.id
