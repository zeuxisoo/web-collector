# coding: utf-8

from flask import Blueprint
from flask import render_template
from sqlalchemy.sql import func
from ..models import Stream

blueprint = Blueprint('stream', __name__)

@blueprint.route('/image/<int:result_id>-<name>')
def image(result_id, name):
    stream = Stream.query.filter_by(result_id=result_id).first()
    random = Stream.query.order_by(func.random()).offset(0).limit(12).all()

    return render_template('stream/image.html', stream=stream, random=random)
