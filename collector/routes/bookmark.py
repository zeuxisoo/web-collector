# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, flash, redirect, url_for
from ..models import db, Stream, Bookmark, Today
from ..helpers.value import force_integer
from ..helpers.user import require_login
from ..helpers.bookmark import is_bookmarked

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/', defaults={ 'category': 'stream' })
@blueprint.route('/<category>')
@require_login
def index(category):
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        if category == 'stream':
            paginator = Stream.query.outerjoin(Bookmark, Bookmark.target_id == Stream.result_id).filter(
                Bookmark.category == 'stream',
                Bookmark.user_id == g.user.id,
            ).order_by(Bookmark.create_at.desc()).paginate(page)

            total_bookmark = Bookmark.query.filter_by(category='stream', user_id=g.user.id).count()
            random_images  = Stream.randomly(0, 6)
        elif category == 'today':
            paginator = Today.query.outerjoin(Bookmark, Bookmark.target_id == Today.result_id).filter(
                Bookmark.category == 'today',
                Bookmark.user_id == g.user.id,
            ).order_by(Bookmark.create_at.desc()).paginate(page)

            total_bookmark = Bookmark.query.filter_by(category='today', user_id=g.user.id).count()
            random_images  = Today.randomly(0, 6)

        return render_template('bookmark/index.html', paginator=paginator, total_bookmark=total_bookmark, random_images=random_images, category=category)

@blueprint.route('/detail/<category>/<int:result_id>-<name>')
def detail(category, result_id, name):
    user_id = g.user.id if g.user else None

    if category == 'stream':
        model  = Stream.query.filter_by(result_id=result_id).first()
        random = Stream.randomly(0, 12)

        # Find user bookmarks, mark it is subquery, temp table
        user_bookmarks_subquery = Stream.query.outerjoin(Bookmark, Bookmark.target_id == Stream.result_id).filter(
            Bookmark.category == 'stream',
            Bookmark.user_id == user_id,
        ).order_by(Bookmark.create_at.desc()).subquery()
    elif category == 'today':
        model  = Today.query.filter_by(result_id=result_id).first()
        random = Today.randomly(0, 12)

        # Find user bookmarks, mark it is subquery, temp table
        user_bookmarks_subquery = Today.query.outerjoin(Bookmark, Bookmark.target_id == Today.result_id).filter(
            Bookmark.category == 'today',
            Bookmark.user_id == user_id,
        ).order_by(Bookmark.create_at.desc()).subquery()

    # Set query object in the temp table user_bookmark_subquery (step 1 marked)
    user_bookmarks_query = db.session.query(user_bookmarks_subquery)

    # Find out next and previous record in query object user_bookmarks_query (step 2 marked)
    old_new = user_bookmarks_query.filter(
        db.or_(
            user_bookmarks_subquery.c.result_id == user_bookmarks_query.with_entities(db.func.min(user_bookmarks_subquery.c.result_id).label('min')).filter(user_bookmarks_subquery.c.result_id > model.result_id),
            user_bookmarks_subquery.c.result_id == user_bookmarks_query.with_entities(db.func.max(user_bookmarks_subquery.c.result_id).label('max')).filter(user_bookmarks_subquery.c.result_id < model.result_id)
        )
    ).all()

    return render_template('bookmark/detail.html', model=model, random=random, bookmarked=is_bookmarked(category, model.result_id, user_id), old_new=old_new, category=category)

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
