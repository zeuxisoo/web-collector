# coding: utf-8

from flask import Blueprint
from flask import current_app, jsonify, url_for
from ..filters import Embedly

blueprint = Blueprint('ajax', __name__)

@blueprint.route('/today-girl')
def today_girl():
    today_girl     = current_app.curator.today()
    today_result   = today_girl.today_result()
    embedly_filter = Embedly(current_app.config.get('EMBEDLY_API_TOKEN'))

    today_result['image'] = embedly_filter.fill('stream', today_result['image'], 230, 230, 'FFF', True)
    today_result['href']  = url_for('today.detail', result_date=today_result['date'], result_id=today_result['id'], name=today_result['name'])

    return jsonify(today_result)
