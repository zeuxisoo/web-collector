# coding: utf-8

import os
from time import sleep
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
                    self.save_stream(page_result)
                    self.logger.debug("==> Result {0} saved".format(page_result['id']))
                else:
                    same_result_count = same_result_count + 1
                    self.logger.debug("Get same data, leave the page result list")
                    break

                sleep(1)

            if same_result_count >= 5:
                self.logger.debug("Same data count equals 5 times, break the page list")
                break

        self.logger.debug("Latest record was updated")
