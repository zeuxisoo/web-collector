# coding: utf-8

import functools
from flask import Blueprint, g
from flask import url_for, redirect, flash
from ..models import Stream, Today, Comment
from ..forms import CommentForm
from ..helpers.user import require_login

blueprint = Blueprint('comment', __name__)

@blueprint.route('/create/<category>/<result_id>/<page_name>', methods=['POST'])
@require_login
def create(category, result_id, page_name):
    models = {
        'stream': Stream,
        'today' : Today
    }

    return_urls = {
        'stream'  : functools.partial(url_for, 'stream.detail'),
        'today'   : functools.partial(url_for, 'today.detail'),
        'bookmark': functools.partial(url_for, 'bookmark.detail')
    }

    # Find matched model object and return_url method
    Model      = models[category]
    return_url = return_urls[page_name]

    # Find record by result_id, create comment form and default params for return url
    model  = Model.query.filter_by(result_id=result_id).first_or_404()
    form   = CommentForm()
    params = {
        'result_id': model.result_id,
        'name'     : model.result_name
    }

    # Update the params for different url
    if page_name == 'today':
        params['result_date'] = model.result_date
    elif page_name == 'bookmark':
        params['category'] = category

    # Validate form submition
    if form.validate_on_submit():
        form.save(category, result_id, g.user)
        flash('Your comment submitted', 'success')
    else:
        flash(form.errors['content'][0], 'error')

    # Redirect page
    return redirect(return_url(**params))
