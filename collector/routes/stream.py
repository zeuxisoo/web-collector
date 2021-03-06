# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, abort, flash, redirect, url_for
from ..models import db, Stream, Comment
from ..forms import CommentForm
from ..helpers.value import force_integer, fill_with_users
from ..helpers.bookmark import is_bookmarked
from ..helpers.user import require_login

blueprint = Blueprint('stream', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator  = Stream.query.order_by(Stream.result_created_at.desc()).paginate(page)
        total_girl = Stream.query.count()

        return render_template('stream/index.html', paginator=paginator, total_girl=total_girl)

@blueprint.route('/detail/<int:result_id>-<path:name>')
def detail(result_id, name):
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        stream  = Stream.query.filter_by(result_id=result_id).first()
        random  = Stream.randomly(0, 12)

        if g.user:
            user_id      = g.user.id
            comment_form = CommentForm()
        else:
            user_id      = None
            comment_form = None

        old_new = Stream.query.filter(
            db.or_(
                Stream.result_id == Stream.query.with_entities(db.func.min(Stream.result_id).label('min')).filter(Stream.result_id > stream.result_id),
                Stream.result_id == Stream.query.with_entities(db.func.max(Stream.result_id).label('max')).filter(Stream.result_id < stream.result_id)
            )
        ).order_by(Stream.result_created_at.desc()).all()

        comment_paginator       = Comment.query.filter_by(category='stream', result_id=result_id).paginate(page)
        comment_paginator.items = fill_with_users(comment_paginator.items)

        return render_template('stream/detail.html', stream=stream, random=random, bookmarked=is_bookmarked('stream', stream.result_id, user_id), old_new=old_new, comment_form=comment_form, comment_paginator=comment_paginator)
