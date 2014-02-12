#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask
from .routes import index

def create_app(config=None):
    app = Flask(__name__, template_folder='views')
    app.static_folder = os.path.abspath('static')

    app.config.from_pyfile('configs/default.py')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_route(app)

    return app

def register_route(app):
    app.register_blueprint(index.blueprint, url_prefix='')
