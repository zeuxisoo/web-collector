# coding: utf-8

import os
import logging
from dateutil import parser
from flask import current_app
from ..curators import API
from ..models import Stream, Today, TodayDetail

class BaseCommand(object):

    def get_curator_api(self):
        return API(current_app.config.get('CURATORS_API_TOKEN'))

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger_stream_handler = logging.StreamHandler()
        logger_stream_handler.setLevel(logging.DEBUG)
        logger_stream_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_stream_handler)

        return logger

    def save_stream(self, result):
        return Stream(
            result_id               = result['id'],
            result_name             = result['name'],
            result_thumbnail        = result['thumbnail'],
            result_thumbnail_width  = result['thumbnail_width'],
            result_thumbnail_height = result['thumbnail_height'],
            result_image            = result['image'],
            result_width            = result['width'],
            result_height           = result['height'],
            result_created_at       = parser.parse(result['created_at']),
            filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])
        ).save()

    def save_today(self, result):
        return Today(
            result_id               = result['id'],
            result_name             = result['name'],
            result_image            = result['image'],
            result_width            = result['width'],
            result_height           = result['height'],
            result_thumbnail        = result['thumbnail'],
            result_thumbnail_width  = result['thumbnail_width'],
            result_thumbnail_height = result['thumbnail_height'],
            result_date             = parser.parse(result['date']),
            filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])
        ).save()

    def save_today_detail(self, today_date, result):
        return TodayDetail(
            today_date              = today_date,
            result_id               = result['id'],
            result_name             = result['name'],
            result_thumbnail        = result['thumbnail'],
            result_thumbnail_width  = result['thumbnail_width'],
            result_thumbnail_height = result['thumbnail_height'],
            result_image            = result['image'],
            result_width            = result['width'],
            result_height           = result['height'],
            result_created_at       = parser.parse(result['created_at']),
            filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])
        ).save()

    def update_stream_image(self, result):
        stream = Stream.query.filter_by(result_id=result['id']).first()

        if stream:
            stream.result_thumbnail        = result['thumbnail']
            stream.result_thumbnail_width  = result['thumbnail_width']
            stream.result_thumbnail_height = result['thumbnail_height']
            stream.result_image            = result['image']
            stream.result_width            = result['width']
            stream.result_height           = result['height']
            stream.filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])

            stream.save()

            return stream
        else:
            return None

    def update_today_image(self, result):
        today = Today.query.filter_by(result_id=result['id']).first()

        if today:
            today.result_image            = result['image']
            today.result_width            = result['width']
            today.result_height           = result['height']
            today.result_thumbnail        = result['thumbnail']
            today.result_thumbnail_width  = result['thumbnail_width']
            today.result_thumbnail_height = result['thumbnail_height']
            today.filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])

            today.save()

            return today
        else:
            return None

    def update_today_detail_image(self, today_date, result):
        today_detail = TodayDetail.query.filter_by(today_date=today_date, result_id=result['id']).first()

        if today_detail:
            today_detail.result_id               = result['id']
            today_detail.result_thumbnail        = result['thumbnail']
            today_detail.result_thumbnail_width  = result['thumbnail_width']
            today_detail.result_thumbnail_height = result['thumbnail_height']
            today_detail.result_image            = result['image']
            today_detail.result_width            = result['width']
            today_detail.result_height           = result['height']
            today_detail.filename                = "{0}{1}".format(result['id'], os.path.splitext(result['image'])[1])

            today_detail.save()

            return today_detail
        else:
            return None
