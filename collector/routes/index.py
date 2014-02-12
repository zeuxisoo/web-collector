# coding: utf-8

import os
from flask import Blueprint
from flask import render_template, request, abort
from ..models import Stream
from ..helpers.value import force_integer

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator = Stream.query.order_by(Stream.result_created_at.desc()).paginate(page)

        return render_template('index.html', paginator=paginator)
