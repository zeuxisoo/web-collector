# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, flash, redirect, url_for, abort
from ..models import db, Stream, Bookmark, Today, UserConnection
from ..helpers.value import force_integer
from ..helpers.user import require_login
from ..helpers.bookmark import is_bookmarked
from ..tasks.stream import save_to_dropbox as save_stream_to_dropbox
from ..tasks.today import save_to_dropbox as save_today_to_dropbox

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/', defaults={ 'category': 'stream' })
@blueprint.route('/<category>')
@require_login
def index(category):
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    elif category not in ['stream', 'today']:
        return abort(400, 'Bookmark category does not match in index page')
    else:
        if category == 'stream':
            Model = Stream
        elif category == 'today':
            Model = Today

        paginator = Model.query.outerjoin(Bookmark, Bookmark.target_id == Model.result_id).filter(
            Bookmark.category == category,
            Bookmark.user_id == g.user.id,
        ).order_by(Bookmark.create_at.desc()).paginate(page)

        total_bookmark = Bookmark.query.filter_by(category=category, user_id=g.user.id).count()
        random_images  = Model.randomly(0, 6)

        return render_template('bookmark/index.html', paginator=paginator, total_bookmark=total_bookmark, random_images=random_images, category=category)

@blueprint.route('/detail/<category>/<int:result_id>-<path:name>')
def detail(category, result_id, name):
    if category not in ['stream', 'today']:
        return abort(400, 'Bookmark category does not match in index page')
    else:
        user_id = g.user.id if g.user else None

        if category == 'stream':
            Model = Stream
        elif category == 'today':
            Model = Today

        row = Model.query.filter_by(result_id=result_id).first()

        if not row:
            return abort(404)
        else:
            random = Model.randomly(0, 12)

            # Find user bookmarks, mark it is subquery, temp table
            user_bookmarks_subquery = Model.query.outerjoin(Bookmark, Bookmark.target_id == Model.result_id).filter(
                Bookmark.category == category,
                Bookmark.user_id == user_id,
            ).order_by(Bookmark.create_at.desc()).subquery()

            # Set query object in the temp table user_bookmark_subquery (step 1 marked)
            user_bookmarks_query = db.session.query(user_bookmarks_subquery)

            # Find out next and previous record in query object user_bookmarks_query (step 2 marked)
            old_new = user_bookmarks_query.filter(
                db.or_(
                    user_bookmarks_subquery.c.result_id == user_bookmarks_query.with_entities(db.func.min(user_bookmarks_subquery.c.result_id).label('min')).filter(user_bookmarks_subquery.c.result_id > row.result_id),
                    user_bookmarks_subquery.c.result_id == user_bookmarks_query.with_entities(db.func.max(user_bookmarks_subquery.c.result_id).label('max')).filter(user_bookmarks_subquery.c.result_id < row.result_id)
                )
            ).all()

            return render_template('bookmark/detail.html', row=row, random=random, bookmarked=is_bookmarked(category, row.result_id, user_id), old_new=old_new, category=category)

@blueprint.route('/create/stream/<int:result_id>')
@require_login
def create_stream(result_id):
    stream   = Stream.query.filter_by(result_id=result_id).first_or_404()
    bookmark = Bookmark.query.filter_by(category='stream', target_id=result_id, user_id=g.user.id).first()

    if bookmark:
        flash('The girl already bookmarked', 'error')
    else:
        Bookmark(
            category  = 'stream',
            user_id   = g.user.id,
            target_id = result_id
        ).save()

        flash('The girl was bookmarked', 'success')

    return redirect(url_for('stream.detail', result_id=stream.result_id, name=stream.result_name))

@blueprint.route('/remove/stream/<int:result_id>')
@require_login
def remove_stream(result_id):
    stream   = Stream.query.filter_by(result_id=result_id).first_or_404()
    bookmark = Bookmark.query.filter_by(category='stream', target_id=result_id, user_id=g.user.id).first()

    if not bookmark:
        flash('You are not created bookmark on this girl', 'error')
    else:
        bookmark.delete()

        flash('The bookmark was removed', 'success')

    return redirect(url_for('stream.detail', result_id=stream.result_id, name=stream.result_name))

@blueprint.route('/create/today/<int:result_id>')
@require_login
def create_today(result_id):
    today    = Today.query.filter_by(result_id=result_id).first_or_404()
    bookmark = Bookmark.query.filter_by(category='today', target_id=result_id, user_id=g.user.id).first()

    if bookmark:
        flash('The girl already bookmarked', 'error')
    else:
        Bookmark(
            category  = 'today',
            user_id   = g.user.id,
            target_id = result_id
        ).save()

        flash('The girl was bookmarked', 'success')

    return redirect(url_for('today.detail', result_date=today.result_date, result_id=today.result_id, name=today.result_name))

@blueprint.route('/remove/today/<int:result_id>')
@require_login
def remove_today(result_id):
    today    = Today.query.filter_by(result_id=result_id).first_or_404()
    bookmark = Bookmark.query.filter_by(category='today', target_id=result_id, user_id=g.user.id).first()

    if not bookmark:
        flash('You are not created bookmark on this girl', 'error')
    else:
        bookmark.delete()

        flash('The bookmark was removed', 'success')

    return redirect(url_for('today.detail', result_date=today.result_date, result_id=today.result_id, name=today.result_name))

@blueprint.route('/dropbox/<category>/<int:result_id>')
@require_login
def dropbox(category, result_id):
    if category not in ['stream', 'today']:
        return abort(400, 'Bookmark category does not match in index page')
    else:
        if category == 'stream':
            Model = Stream
            task  = save_stream_to_dropbox
        elif category == 'today':
            Model = Today
            task  = save_today_to_dropbox

        row             = Model.query.filter_by(result_id=result_id).first()
        user_connection = UserConnection.query.filter_by(user_id=g.user.id, provider_name='dropbox').first()

        if not row:
            flash('Can not found the bookmarked image', 'error')
        elif not user_connection:
            flash('Please enable dropbox connection in your account settings page', 'error')
        else:
            task.apply_async((g.user.id, result_id))

            flash('Bookmarked image is sending to your dropbox, Please check again after a while', 'success')

        return redirect(url_for('bookmark.detail', category=category, result_id=row.result_id, name=row.result_name))
