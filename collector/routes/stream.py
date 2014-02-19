# coding: utf-8

from flask import Blueprint, g
from flask import render_template, flash, redirect, url_for
from ..models import db, Stream, UserConnection
from ..helpers.bookmark import is_bookmarked
from ..helpers.user import require_login
from ..tasks.stream import save_to_dropbox

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

@blueprint.route('/dropbox/<int:result_id>')
@require_login
def dropbox(result_id):
    stream          = Stream.query.filter_by(result_id=result_id).first()
    user_connection = UserConnection.query.filter_by(user_id=g.user.id, provider_name='dropbox').first()

    if not stream:
        flash('Can not found the stream image', 'error')
    elif not user_connection:
        flash('Please enable dropbox connection in your account settings page', 'error')
    else:
        save_to_dropbox.apply_async((g.user.id, result_id))

        flash('Stream image is sending to your dropbox, Please check again after a while', 'success')

    return redirect(url_for('stream.detail', result_id=stream.result_id, name=stream.result_name))
