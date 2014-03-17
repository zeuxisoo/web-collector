# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, abort, flash, redirect, url_for
from ..models import db, Today, Comment
from ..forms import CommentForm
from ..helpers.value import force_integer, fill_with_users
from ..helpers.bookmark import is_bookmarked
from ..helpers.user import require_login

blueprint = Blueprint('today', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator  = Today.query.order_by(Today.result_date.desc()).paginate(page)
        total_days = Today.query.count()

        return render_template('today/index.html', paginator=paginator, total_days=total_days)

@blueprint.route('/detail/<result_date>/<int:result_id>-<path:name>')
def detail(result_date, result_id, name):
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        today   = Today.query.filter_by(result_id=result_id).first()
        random  = Today.randomly(0, 12)

        if g.user:
            user_id      = g.user.id
            comment_form = CommentForm()
        else:
            user_id      = None
            comment_form = None

        old_new = Today.query.filter(
            db.or_(
                Today.result_date == Today.query.with_entities(db.func.min(Today.result_date).label('min')).filter(Today.result_date > today.result_date),
                Today.result_date == Today.query.with_entities(db.func.max(Today.result_date).label('max')).filter(Today.result_date < today.result_date)
            )
        ).order_by(Today.result_date.desc()).all()

        comment_paginator       = Comment.query.filter_by(category='today', result_id=result_id).paginate(page)
        comment_paginator.items = fill_with_users(comment_paginator.items)

        return render_template('today/detail.html', today=today, random=random, bookmarked=is_bookmarked('today', today.result_id, user_id), old_new=old_new, comment_form=comment_form, comment_paginator=comment_paginator)
