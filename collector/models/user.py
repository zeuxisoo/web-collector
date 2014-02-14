# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime
from werkzeug import security
from flask.ext.bcrypt import Bcrypt

class User(db.Model, SessionMixin):
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email     = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password  = db.Column(db.String(60))
    token     = db.Column(db.String(20))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        self.token = self.generate_token(18)

        if 'email' in kwargs:
            self.email = kwargs.pop('email').lower()

        if 'password' in kwargs:
            self.password = self.password_hash(kwargs.pop('password'))

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User: %s>' % self.email

    def change_password(self, new_password):
        self.password = self.password_hash(new_password)
        self.token    = self.generate_token(18)

    @staticmethod
    def generate_token(length=18):
        return security.gen_salt(length)

    @staticmethod
    def password_hash(password, rounds=None):
        return Bcrypt().generate_password_hash(password, rounds=rounds)

    @staticmethod
    def password_verify(password, password_hash):
        return Bcrypt().check_password_hash(password_hash, password)
