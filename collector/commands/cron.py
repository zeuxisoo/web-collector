# coding: utf-8

import os
from time import sleep
from flask import current_app
from dateutil import parser
from ..models import db, Stream, Today, TodayDetail
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

class CronToday(BaseCommand):

    def __init__(self):
        self.curator_api  = self.get_curator_api()
        self.latest_today = self.get_latest_today()
        self.logger       = self.get_logger()

        self.logger.debug("Latest today")
        self.logger.debug("==> result date: {0}".format(self.latest_today.result_date))

    def get_latest_today(self):
        return Today.query.filter_by(
            result_date = Today.query.with_entities(db.func.max(Today.result_date))
        ).first()

    def make(self):
        today = self.curator_api.today()

        same_result_count = 0

        for page in range(1, today.total_pages() + 1):
            self.logger.debug("Getting page no: {0}".format(page))

            page_today   = self.curator_api.today(page)
            page_results = page_today.results()

            for page_result in page_results:
                page_date   = parser.parse(page_result['date']).date()
                result_date = self.latest_today.result_date

                if page_date > result_date:
                    self.logger.debug("==> {0} > {1}".format(page_result['date'], self.latest_today.result_date))
                    self.save_today(page_result)
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

class CronTodayDetail(BaseCommand):

    def __init__(self):
        self.curator_api         = self.get_curator_api()
        self.logger              = self.get_logger()

        self.logger.debug("Latest today detail")

    def make(self):
        # Get latest today_date from today_detail table
        today_detail = TodayDetail.query.filter_by(
            today_date = TodayDetail.query.with_entities(db.func.max(TodayDetail.today_date))
        ).first()

        self.logger.debug("==> latest today date: {0}".format(today_detail.today_date))

        # Find all new date by condition today.result_date is newest than today_detail.today_date
        # new_today = Today.query.filter(Today.result_date > '2014-03-03').all()
        new_today = Today.query.filter(Today.result_date > today_detail.today_date).all()
        new_dates = [today.result_date for today in new_today]

        # Fetch the images from new date page into today_detail table
        for new_date in new_dates:
            self.logger.debug("Getting date string: {0}".format(new_date))

            today_detail = self.curator_api.today_detail(new_date)

            for page_result in today_detail.results():
                self.save_today_detail(new_date, page_result)
                self.logger.debug("==> Result {0} saved".format(page_result['id']))

        self.logger.debug("Latest record was updated")