# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Bookmark(db.Model, SessionMixin):
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category  = db.Column(db.Enum('stream', 'the_of_girl'), nullable=False, default='stream')
    user_id   = db.Column(db.Integer, index=True)
    target_id = db.Column(db.Integer, index=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Support for
    # - User.query.get(1).bookmarks
    # - Bookmark.query.get(1).user
    user = db.relationship('User', backref='bookmarks', primaryjoin="Bookmark.user_id == User.id", foreign_keys=[user_id])

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Bookmark: %s>' % self.id
