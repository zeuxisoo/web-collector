# coding: utf-8

from flask import Blueprint, g
from flask import render_template, request, abort, flash, redirect, url_for
from ..models import db, Today, UserConnection
from ..helpers.value import force_integer
from ..helpers.bookmark import is_bookmarked
from ..helpers.user import require_login
from ..tasks.today import save_to_dropbox

blueprint = Blueprint('today', __name__)

@blueprint.route('/')
def index():
    page = force_integer(request.args.get('page', 1), 0)

    if not page:
        return abort(404)
    else:
        paginator  = Today.query.order_by(Today.result_date.desc()).paginate(page)

        return render_template('today/index.html', paginator=paginator)

@blueprint.route('/detail/<result_date>/<int:result_id>-<path:name>')
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

    return render_template('today/detail.html', today=today, random=random, bookmarked=is_bookmarked('today', today.result_id, user_id), old_new=old_new)

@blueprint.route('/dropbox/<int:result_id>')
@require_login
def dropbox(result_id):
    today           = Today.query.filter_by(result_id=result_id).first()
    user_connection = UserConnection.query.filter_by(user_id=g.user.id, provider_name='dropbox').first()

    if not today:
        flash('Can not found the today image', 'error')
    elif not user_connection:
        flash('Please enable dropbox connection in your account settings page', 'error')
    else:
        save_to_dropbox.apply_async((g.user.id, result_id))

        flash('Today image is sending to your dropbox, Please check again after a while', 'success')

    return redirect(url_for('today.detail', result_date=today.result_date, result_id=today.result_id, name=today.result_name))
