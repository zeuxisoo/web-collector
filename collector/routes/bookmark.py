# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, flash, redirect, url_for
from ..models import db, Stream, Bookmark
from ..helpers.value import force_integer
from ..helpers.user import require_login

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/')
@require_login
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator = Stream.query.outerjoin(Bookmark, Bookmark.target_id == Stream.id).filter(
            Bookmark.category == 'stream',
            Bookmark.user_id == g.user.id,
        ).order_by(Bookmark.create_at.desc()).paginate(page)

        total_bookmark = Bookmark.query.filter_by(category='stream', user_id=g.user.id).count()
        random_stream  = Stream.randomly(0, 6)

        return render_template('bookmark/index.html', paginator=paginator, total_bookmark=total_bookmark, random_stream=random_stream)

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

    return redirect(url_for('stream.detail', result_id=stream.result_id, name=stream.result_name))

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

    return redirect(url_for('stream.detail', result_id=stream.result_id, name=stream.result_name))
