# coding: utf-8

import os
from flask import Blueprint
from flask import render_template, request, abort, current_app
from ..models import db, Stream, Today
from ..helpers.value import force_integer

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        latest_streams = Stream.query.order_by(Stream.result_created_at.desc()).offset(0).limit(24).all()
        latest_todays  = Today.query.order_by(Today.result_date.desc()).offset(0).limit(24).all()

        random_streams = Stream.randomly(0, 6)
        random_todays  = Today.randomly(0, 6)

        total_images   = Stream.query.count() + Today.query.count()

        return render_template('index.html', latest_streams=latest_streams, latest_todays=latest_todays, random_streams=random_streams, random_todays=random_todays, total_images=total_images)
