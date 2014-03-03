# coding: utf-8

from math import ceil
from decimal import Decimal

class Today(object):

    def __init__(self, response):
        self.response = response
        self.json     = response.json()

    def count(self):
        return self.json['count']

    def next(self):
        return self.json['next']

    def previous(self):
        return self.json['previous']

    def results(self):
        return self.json['results']

    def total_results(self):
        return len(self.results())

    def total_pages(self):
        return int(ceil(self.count() / Decimal(self.total_results())))

    def find_result_by_id(self, id_):
        for result in self.results():
            if result['id'] == int(id_):
                return result

        return None

    def today_result(self):
        return self.results()[0]

class TodayDetail(object):

    def __init__(self, response):
        self.response = response
        self.json     = response.json()

    def results(self):
        return self.json

    def total_results(self):
        return len(self.results())

    def find_result_by_id(self, id_):
        for result in self.results():
            if result['id'] == int(id_):
                return result

        return None
