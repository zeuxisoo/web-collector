# coding: utf-8

import os
from flask import Blueprint, g
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

@blueprint.route('/detail/<result_date>/<int:result_id>-<name>')
def detail(result_date, result_id, name):
    today   = Today.query.filter_by(result_id=result_id).first()
    random  = Today.randomly(0, 12)
    user_id = g.user.id if g.user else None

    old_new = Today.query.filter(
        db.or_(
            Today.result_date == Today.query.with_entities(db.func.min(Today.result_date).label('min')).filter(Today.result_date > today.result_date),
            Today.result_date == Today.query.with_entities(db.func.max(Today.result_date).label('max')).filter(Today.result_date < today.result_date)
        )
    ).order_by(Today.result_date.desc()).all()

    return render_template('today/detail.html', today=today, random=random, old_new=old_new)
