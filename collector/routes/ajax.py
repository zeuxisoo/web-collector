# coding: utf-8

from flask import Blueprint
from flask import current_app, jsonify
from ..filters import Embedly

blueprint = Blueprint('ajax', __name__)

@blueprint.route('/today-girl')
def today_girl():
    today_girl     = current_app.curator.girl_of_the_day()
    today_result   = today_girl.today_result()
    embedly_filter = Embedly(current_app.config.get('EMBEDLY_API_TOKEN'))

    today_result['image'] = embedly_filter.fill(today_result['image'], 240, 240, 'FFF', True)

    return jsonify(today_result)
