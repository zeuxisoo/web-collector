# coding: utf-8

import os
from flask import Blueprint
from flask import render_template, request, abort
from ..models import db, Today
from ..helpers.value import force_integer

blueprint = Blueprint('today', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator  = Today.query.order_by(Today.result_date.desc()).paginate(page)

        return render_template('today/index.html', paginator=paginator)
