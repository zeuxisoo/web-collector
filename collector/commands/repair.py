# coding: utf-8

from time import sleep
from itertools import chain
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from ..helpers.watcher import Watcher
from .base import BaseCommand

class RepairStreamImage(BaseCommand):

    def __init__(self):
        self.curator_api = self.get_curator_api()
        self.logger      = self.get_logger()

    def get_page_nos(self):
        return [page_no for page_no in range(1, self.curator_api.stream().total_pages() + 1)]

    def save_page_results(self, page_no):
        self.logger.debug("Getting page no: {0}".format(page_no))

        stream = self.curator_api.stream(page_no)

        for result in stream.results():
            self.logger.debug("==> Stream {0}".format(result['id']))

            stream = self.update_stream_image(result)

            if stream:
                self.logger.debug("====> updated")
            else:
                self.logger.debug("====> no exists")

            sleep(0.001)

    def make(self):
        page_nos = self.get_page_nos()

        Watcher()
        pool = Pool(cpu_count())
        pool.map(self.save_page_results, page_nos)
        pool.close()
        pool.join()

class RepairTodayImage(BaseCommand):
    def __init__(self):
        self.curator_api = self.get_curator_api()
        self.logger      = self.get_logger()

    def get_page_nos(self):
        return [page_no for page_no in range(1, self.curator_api.today().total_pages() + 1)]

    def save_page_results(self, page_no):
        self.logger.debug("Getting page no: {0}".format(page_no))

        today = self.curator_api.today(page_no)

        for result in today.results():
            self.logger.debug("==> Today {0}".format(result['id']))

            today = self.update_today_image(result)

            if today:
                self.logger.debug("====> updated")
            else:
                self.logger.debug("====> no exists")

            sleep(0.001)

    def make(self):
        page_nos = self.get_page_nos()

        Watcher()
        pool = Pool(cpu_count())
        pool.map(self.save_page_results, page_nos)
        pool.close()
        pool.join()
