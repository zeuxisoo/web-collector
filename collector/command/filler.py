# coding: utf-8

import os
import requests
from time import sleep
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from dateutil import parser
from ..models import Stream
from ..helpers.watcher import Watcher
from .base import BaseCommand

class FillStream(BaseCommand):

    def __init__(self):
        self.curator_api = self.get_curator_api()
        self.logger      = self.get_logger()

    def get_page_nos(self):
        return [page_no for page_no in range(1, self.curator_api.stream().total_pages() + 1)]

    def save_page_results(self, page_no):
        self.logger.debug("Getting page no: {0}".format(page_no))

        stream = self.curator_api.stream(page_no)

        for result in stream.results():
            try:
                Stream(
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
                self.logger.debug("==> Result {0} saved".format(result['id']))
            except IntegrityError:
                self.logger.debug("==> Result {0} already exists (unique)".format(result['id']))
            except InvalidRequestError:
                self.logger.debug("==> Result {0} already exists (rollback)".format(result['id']))
            sleep(0.001)

    def make(self):
        page_nos = self.get_page_nos()

        Watcher()
        pool = Pool(cpu_count())
        pool.map(self.save_page_results, page_nos)
        pool.close()
        pool.join()
