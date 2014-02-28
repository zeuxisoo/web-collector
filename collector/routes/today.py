# coding: utf-8

import os
from flask import Blueprint
from flask import render_template, request, abort, current_app
from ..models import db, Stream
from ..helpers.value import force_integer

blueprint = Blueprint('today', __name__)

@blueprint.route('/')
def index():
    return render_template('today/index.html')
