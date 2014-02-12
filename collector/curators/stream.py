# coding: utf-8

from math import ceil
from decimal import Decimal

class Stream(object):

    def __init__(self, response):
        self.response = response
        self.json     = response.json()

    def count(self):
        return self.json['count']

    def next(self):
        return self.json['next']

    def previous(self):
        return self.json['previous']

    def results(self, limit=None):
        if limit is None:
            return self.json['results']
        else:
            return self.json['results'][0:limit]

    def total_results(self):
        return len(self.results())

    def total_pages(self):
        return int(ceil(self.count() / Decimal(self.total_results())))

    def find_result_by_id(self, id):
        for result in self.results():
            if result['id'] == id:
                return result

        return None
