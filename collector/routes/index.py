# coding: utf-8

import os
from flask import Blueprint
from flask import render_template, request, abort, current_app, send_from_directory
from ..models import db, Stream, Today
from ..helpers.value import force_integer

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        limit = 30 if current_app.config.get('GOOGLE_ADSENSE')['slidebar']['enable'] else 24

        latest_streams = Stream.query.order_by(Stream.result_created_at.desc()).offset(0).limit(limit).all()
        latest_todays  = Today.query.order_by(Today.result_date.desc()).offset(0).limit(limit).all()

        random_streams = Stream.randomly(0, 6)
        random_todays  = Today.randomly(0, 6)

        total_images   = Stream.query.count() + Today.query.count()

        return render_template('index.html', latest_streams=latest_streams, latest_todays=latest_todays, random_streams=random_streams, random_todays=random_todays, total_images=total_images)

@blueprint.route('/robots.txt')
@blueprint.route('/sitemap.xml')
def send_specific_file():
    return send_from_directory(current_app.static_folder, request.path[1:])
