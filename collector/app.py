#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, g
from flask.ext.oauthlib.client import OAuth
from .models import db
from .routes import index, user, stream, bookmark, ajax, oauth, today, comment, dropbox
from .helpers.user import get_current_user
from .filters import Embedly, SocialButton, Clock
from .curators import API
from .tasks import make_celery

def create_app(config=None):
    app = Flask(__name__, template_folder='views')
    app.static_folder = os.path.abspath('static')

    app.config.from_pyfile('configs/default.py')

    production_config = os.path.join(os.path.dirname(__file__), 'configs/production.py')
    if os.path.exists(production_config):
        app.config.from_pyfile(production_config)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_hook(app)
    register_celery(app)
    register_celery_beat(app)
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

def register_celery(app):
    app.celery = make_celery(app)

def register_celery_beat(app):
    # import cron job task for beat
    from .tasks.schedule import create_sitemap, create_latest

def register_oauth(app):
    oauth    = OAuth(app)
    dropbox  = oauth.remote_app('dropbox', app_key='DROPBOX')
    facebook = oauth.remote_app('facebook', app_key='FACEBOOK')

    app.oauth = oauth
    app.oauth.providers = {
        'dropbox' : dropbox,
        'facebook': facebook,
    }

def register_curator(app):
    app.curator = API(app.config.get('CURATORS_API_TOKEN'))

def register_jinja2(app):
    app.jinja_env.filters['embedly_fill']             = Embedly(app.config.get('EMBEDLY_API_TOKEN')).fill
    app.jinja_env.filters['embedly_fill_archive_url'] = Embedly(app.config.get('EMBEDLY_API_TOKEN')).fill_archive_url
    app.jinja_env.filters['social_button']            = SocialButton(app.config.get('SOCIAL_BUTTON')).create
    app.jinja_env.filters['clock_humanize']           = Clock().humanize
    app.jinja_env.filters['clock_xml_format']         = Clock().xml_format

def register_database(app):
    db.init_app(app)
    db.app = app

def register_route(app):
    app.register_blueprint(dropbox.blueprint, url_prefix='/dropbox')
    app.register_blueprint(comment.blueprint, url_prefix='/comment')
    app.register_blueprint(oauth.blueprint, url_prefix='/oauth')
    app.register_blueprint(ajax.blueprint, url_prefix='/ajax')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(today.blueprint, url_prefix='/today')
    app.register_blueprint(stream.blueprint, url_prefix='/stream')
    app.register_blueprint(user.blueprint, url_prefix='/user')
    app.register_blueprint(index.blueprint, url_prefix='')
