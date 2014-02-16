# coding: utf-8

from flask import Blueprint, g
from flask import render_template
from ..models import db, Stream
from ..helpers.bookmark import is_bookmarked

blueprint = Blueprint('stream', __name__)

@blueprint.route('/detail/<int:result_id>-<name>')
def detail(result_id, name):
    stream  = Stream.query.filter_by(result_id=result_id).first()
    random  = Stream.randomly(0, 12)
    user_id = g.user.id if g.user else None

    old_new = Stream.query.filter(
        db.or_(
            Stream.result_id == Stream.query.with_entities(db.func.min(Stream.result_id).label('min')).filter(Stream.result_id > stream.result_id),
            Stream.result_id == Stream.query.with_entities(db.func.max(Stream.result_id).label('max')).filter(Stream.result_id < stream.result_id)
        )
    ).order_by(Stream.result_created_at.desc()).all()

    return render_template('stream/detail.html', stream=stream, random=random, bookmarked=is_bookmarked('stream', stream.id, user_id), old_new=old_new)
