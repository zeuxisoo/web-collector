# coding: utf-8

from flask import Blueprint, g
from flask import flash, redirect, url_for
from ..models import Stream, Bookmark
from ..helpers.user import require_login

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/create/stream/<int:stream_id>')
@require_login
def create_stream(stream_id):
    stream   = Stream.query.get_or_404(stream_id)
    bookmark = Bookmark.query.filter_by(category='stream', target_id=stream_id, user_id=g.user.id).first()

    if bookmark:
        flash('The girl already bookmarked', 'error')
    else:
        Bookmark(
            category  = 'stream',
            user_id   = g.user.id,
            target_id = stream_id
        ).save()

        flash('The girl was bookmarked', 'success')

    return redirect(url_for('stream.index', result_id=stream.result_id, name=stream.result_name))

@blueprint.route('/remove/stream/<int:stream_id>')
@require_login
def remove_stream(stream_id):
    stream   = Stream.query.get_or_404(stream_id)
    bookmark = Bookmark.query.filter_by(category='stream', target_id=stream_id, user_id=g.user.id).first()

    if not bookmark:
        flash('You are not created bookmark on this girl', 'error')
    else:
        bookmark.delete()

        flash('The bookmark was removed', 'success')

    return redirect(url_for('stream.index', result_id=stream.result_id, name=stream.result_name))
