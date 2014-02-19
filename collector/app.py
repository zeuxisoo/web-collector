#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask
from flask import g
from flask.ext.oauthlib.client import OAuth
from .models import db
from .routes import index, user, stream, bookmark, ajax, oauth
from .helpers.user import get_current_user
from .filters import Embedly
from .curators import API

def create_app(config=None):
    app = Flask(__name__, template_folder='views')
    app.static_folder = os.path.abspath('static')

    app.config.from_pyfile('configs/default.py')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_hook(app)
    register_oauth(app)
    register_curator(app)
    register_jinja2(app)
    register_database(app)
    register_route(app)

    return app

def register_hook(app):
    @app.before_request
    def load_current_user():
        g.user = get_current_user()

def register_oauth(app):
    oauth   = OAuth(app)
    dropbox = oauth.remote_app('dropbox', app_key='DROPBOX')

    app.oauth = oauth
    app.oauth.providers = {
        'dropbox': dropbox
    }

def register_curator(app):
    app.curator = API(app.config.get('CURATORS_API_TOKEN'))

def register_jinja2(app):
    app.jinja_env.filters['embedly_fill'] = Embedly(app.config.get('EMBEDLY_API_TOKEN')).fill

def register_database(app):
    db.init_app(app)
    db.app = app

def register_route(app):
    app.register_blueprint(oauth.blueprint, url_prefix='/oauth')
    app.register_blueprint(ajax.blueprint, url_prefix='/ajax')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(stream.blueprint, url_prefix='/stream')
    app.register_blueprint(user.blueprint, url_prefix='/user')
    app.register_blueprint(index.blueprint, url_prefix='')
