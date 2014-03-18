# coding: utf-8

import functools
from flask import Blueprint, g
from flask import url_for, redirect, flash, abort
from ..models import Stream, Today, UserConnection
from ..helpers.user import require_login
from ..tasks.dropbox import sync_image

blueprint = Blueprint('dropbox', __name__)

@blueprint.route('/create/<category>/<result_id>/<page_name>')
@require_login
def create(category, result_id, page_name):
    if category not in ['stream', 'today']:
        return abort(400, 'Image category does not match in dropbox.create page')

    models = {
        'stream': Stream,
        'today' : Today
    }

    return_urls = {
        'stream'  : functools.partial(url_for, 'stream.detail'),
        'today'   : functools.partial(url_for, 'today.detail'),
        'bookmark': functools.partial(url_for, 'bookmark.detail')
    }

    # Find matched model object, send to dropbox task and return_url method
    Model      = models[category]
    return_url = return_urls[page_name]

    # Find record by result_id, dropbox connection and default params for return url
    model           = Model.query.filter_by(result_id=result_id).first()
    user_connection = UserConnection.query.filter_by(user_id=g.user.id, provider_name='dropbox').first()

    params = {
        'result_id': model.result_id,
        'name'     : model.result_name
    }

    # Update the params for different url
    if page_name == 'today':
        params['result_date'] = model.result_date
    elif page_name == 'bookmark':
        params['category'] = category

    # Validate model and connection
    if not model:
        flash('Can not found the image', 'error')
    elif not user_connection:
        flash('Please enable dropbox connection in your account settings page', 'error')
    else:
        sync_image.apply_async((category, g.user.id, result_id))

        flash('Image is sending to your dropbox, Please check again after a while', 'success')

    return redirect(return_url(**params))

