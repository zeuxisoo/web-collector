# coding: utf-8

class Today(object):

    def __init__(self, response):
        self.response = response
        self.json     = response.json()

    def count(self):
        return self.json['count'],

    def next(self):
        return self.json['next'],

    def previous(self):
        return self.json['previous'],

    def results(self):
        return self.json['results']

    def today_result(self):
        return self.results()[0]
