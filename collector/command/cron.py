# coding: utf-8

import os
from time import sleep
from dateutil import parser
from flask import current_app
from ..models import db, Stream
from .base import BaseCommand

class CronStream(BaseCommand):

    def __init__(self):
        self.curator_api   = self.get_curator_api()
        self.latest_stream = self.get_latest_stream()
        self.logger        = self.get_logger()

        self.logger.debug("Latest stream")
        self.logger.debug("==> result id: {0}".format(self.latest_stream.result_id))

    def get_latest_stream(self):
        return Stream.query.filter_by(
            result_id = Stream.query.with_entities(db.func.max(Stream.result_id))
        ).first()

    def make(self):
        stream = self.curator_api.stream()

        same_result_count = 0

        for page in range(1, stream.total_pages() + 1):
            self.logger.debug("Getting page no: {0}".format(page))

            page_stream  = self.curator_api.stream(page)
            page_results = page_stream.results()

            for page_result in page_results:
                if page_result['id'] > self.latest_stream.result_id:
                    Stream(
                        result_id               = page_result['id'],
                        result_name             = page_result['name'],
                        result_thumbnail        = page_result['thumbnail'],
                        result_thumbnail_width  = page_result['thumbnail_width'],
                        result_thumbnail_height = page_result['thumbnail_height'],
                        result_image            = page_result['image'],
                        result_width            = page_result['width'],
                        result_height           = page_result['height'],
                        result_created_at       = parser.parse(page_result['created_at']),
                        filename                = "{0}{1}".format(page_result['id'], os.path.splitext(page_result['image'])[1])
                    ).save()
                    self.logger.debug("==> Result {0} saved".format(page_result['id']))
                else:
                    same_result_count = same_result_count + 1
                    self.logger.debug("Get same data, leave the page result list")
                    break

                sleep(0.001)

            if same_result_count >= 5:
                self.logger.debug("Same data count equals 5 times, break the page list")
                break

        self.logger.debug("Latest record was updated")
