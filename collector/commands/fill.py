# coding: utf-8

import requests
from time import sleep
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from itertools import chain
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
                self.save_stream(result)
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

class FillToday(BaseCommand):

    def __init__(self):
        self.curator_api = self.get_curator_api()
        self.logger      = self.get_logger()

    def get_page_nos(self):
        return [page_no for page_no in range(1, self.curator_api.today().total_pages() + 1)]

    def save_page_results(self, page_no):
        self.logger.debug("Getting page no: {0}".format(page_no))

        today = self.curator_api.today(page_no)

        for result in today.results():
            try:
                self.save_today(result)
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

class FillTodayDetail(BaseCommand):

    def __init__(self):
        self.curator_api = self.get_curator_api()
        self.logger      = self.get_logger()

    def get_all_today_page_nos(self):
        return [page_no for page_no in range(1, self.curator_api.today().total_pages() + 1)]

    def get_all_today_dates(self, page_no):
        today = self.curator_api.today(page_no)

        return [result['date'] for result in today.results()]

    def save_today_detail_page_results(self, today_date):
        self.logger.debug("Getting today detail page date: {0}".format(today_date))

        today_detail = self.curator_api.today_detail(today_date)

        for result in today_detail.results():
            try:
                self.save_today_detail(today_date, result)
                self.logger.debug("==> Result {0} saved".format(result['id']))
            except IntegrityError:
                self.logger.debug("==> Result {0} already exists (unique)".format(result['id']))
            except InvalidRequestError:
                self.logger.debug("==> Result {0} already exists (rollback)".format(result['id']))
            sleep(0.001)

    def make(self):
        all_today_page_nos = self.get_all_today_page_nos()

        Watcher()

        pool  = Pool(cpu_count())
        dates = pool.map(self.get_all_today_dates, all_today_page_nos)
        pool.close()
        pool.join()

        pool  = Pool(cpu_count())
        pool.map(self.save_today_detail_page_results, chain.from_iterable(dates)) # convert dates from 2d to 1d array
        pool.close()
        pool.join()
