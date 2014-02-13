# coding: utf-8

from flask import Blueprint, g
from flask import render_template
from ..models import db, Stream
from ..helpers.bookmark import is_bookmarked

blueprint = Blueprint('stream', __name__)

@blueprint.route('/<int:result_id>-<name>')
def index(result_id, name):
    stream = Stream.query.filter_by(result_id=result_id).first()
    random = Stream.query.order_by(db.func.random()).offset(0).limit(12).all()

    return render_template('stream/index.html', stream=stream, random=random, bookmarked=is_bookmarked('stream', stream.id, g.user.id))
