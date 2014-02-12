#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask
from flask import g
from .models import db
from .routes import index, user
from .helpers.user import get_current_user

def create_app(config=None):
    app = Flask(__name__, template_folder='views')
    app.static_folder = os.path.abspath('static')

    app.config.from_pyfile('configs/default.py')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_hook(app)
    register_database(app)
    register_route(app)

    return app

def register_hook(app):
    @app.before_request
    def load_current_user():
        g.user = get_current_user()

def register_database(app):
    db.init_app(app)
    db.app = app

def register_route(app):
    app.register_blueprint(user.blueprint, url_prefix='/user')
    app.register_blueprint(index.blueprint, url_prefix='')