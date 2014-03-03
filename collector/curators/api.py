#!/usr/bin/env python
# coding: utf-8

import requests
from .stream import Stream
from .today import Today

class API(object):

    stream_url = "http://curator.im/api/stream/"
    today_url  = "http://curator.im/api/girl_of_the_day/"

    def __init__(self, token, format="json"):
        self.token  = token
        self.format = format

    def stream(self, page=1):
        response = requests.get(self.stream_url, params={
            'token' : self.token,
            'format': self.format,
            'page'  : page
        })

        return Stream(response)

    def today(self):
        response = requests.get(self.today_url, params={
            'token' : self.token,
            'format': self.format,
        })

        return Today(response)
