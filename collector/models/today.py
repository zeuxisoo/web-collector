# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Today(db.Model, SessionMixin):
    id                      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result_id               = db.Column(db.Integer, unique=True, index=True)
    result_name             = db.Column(db.String(120))
    result_image            = db.Column(db.String(180))
    result_width            = db.Column(db.SmallInteger)
    result_height           = db.Column(db.SmallInteger)
    result_thumbnail        = db.Column(db.String(180))
    result_thumbnail_width  = db.Column(db.SmallInteger)
    result_thumbnail_height = db.Column(db.SmallInteger)
    result_date             = db.Column(db.Date)
    filename                = db.Column(db.String(80))
    create_at               = db.Column(db.DateTime, default=datetime.utcnow)
    update_at               = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Today: %s>' % self.id

    @classmethod
    def randomly(cls, offset=0, limit=20):
        return cls.query.order_by(db.func.random()).offset(offset).limit(limit).all()
